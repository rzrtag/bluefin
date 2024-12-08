#!/usr/bin/env python3

import sys
import requests
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import json
from typing import Dict, Any, Optional, List, Tuple, Union
import random
import time
import yaml
import backoff
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimit import limits, sleep_and_retry
import hashlib

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
CONFIG_ROOT = Path(__file__).parent / "config"

# Rate limiting configuration
CALLS_PER_MINUTE = 30
ONE_MINUTE = 60

class SSIMFetchError(Exception):
    """Base exception for SaberSim fetch errors."""
    pass

class SSIMAuthError(SSIMFetchError):
    """Authentication related errors."""
    pass

class SSIMRateLimitError(SSIMFetchError):
    """Rate limit related errors."""
    pass

class SSIMDataError(SSIMFetchError):
    """Data validation related errors."""
    pass

@sleep_and_retry
@limits(calls=CALLS_PER_MINUTE, period=ONE_MINUTE)
def make_api_request(url: str, headers: Dict[str, str], data: Dict[str, Any], timeout: int = 30) -> requests.Response:
    """Make rate-limited API request."""
    session = requests.Session()
    session.trust_env = False
    try:
        response = session.post(url, headers=headers, json=data, timeout=timeout)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise SSIMFetchError(f"API request failed: {e}")

def handle_response(response: requests.Response) -> Dict[str, Any]:
    """Handle API response and return JSON data."""
    try:
        if response.status_code == 401:
            raise SSIMAuthError("Authentication failed - token may have expired")
        elif response.status_code == 429:
            raise SSIMRateLimitError("Rate limit exceeded")
        elif response.status_code != 200:
            raise SSIMFetchError(f"API request failed with status {response.status_code}")
        
        data = response.json()
        
        # Validate response structure
        if not isinstance(data, dict):
            raise SSIMDataError("Response is not a dictionary")
            
        if 'players' not in data:
            logging.error(f"Available keys in response: {list(data.keys())}")
            raise SSIMDataError("Response missing 'players' field")
            
        if not isinstance(data['players'], list):
            raise SSIMDataError("'players' field is not a list")
        
        return {
            'players': data['players'],
            'timestamp': data.get('timestamp', str(int(datetime.now().timestamp())))
        }
        
    except (ValueError, AttributeError) as e:
        raise SSIMDataError(f"Failed to parse API response: {e}")

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML files."""
    config_file = CONFIG_ROOT / "config.yaml"
    token_file = CONFIG_ROOT / "ssim_token.yaml"
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    if not token_file.exists():
        raise FileNotFoundError(f"Token file not found: {token_file}")
    
    # Load main config
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Load token config
    with open(token_file) as f:
        token_config = yaml.safe_load(f)
    
    # Merge token config into main config
    config.update(token_config)
    
    # Validate required config fields
    required_fields = ['api_url', 'token', 'slate_id']
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValueError(f"Missing required config fields: {missing_fields}")
    
    return config

def get_cache_file_path(date: str) -> Path:
    """Get path to cache file for a specific date."""
    cache_dir = DATA_ROOT / "nba/ssim/cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{date}_cache.json"

def load_cache(cache_file: Path) -> Dict[str, Any]:
    """Load cached data if it exists."""
    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)
    return {}

def save_cache(cache_file: Path, data: Dict[str, Any]):
    """Save data to cache."""
    with open(cache_file, 'w') as f:
        json.dump(data, f, indent=2)

def get_data_hash(data: Dict[str, Any]) -> str:
    """Calculate hash of data to detect changes."""
    return hashlib.md5(json.dumps(data.get('players', []), sort_keys=True).encode()).hexdigest()

def has_data_changed(new_data: Dict[str, Any], cache_file: Path) -> bool:
    """Check if data has changed compared to cache."""
    if not cache_file.exists():
        return True
        
    cached_data = load_cache(cache_file)
    new_hash = get_data_hash(new_data)
    cached_hash = cached_data.get('hash')
    
    return new_hash != cached_hash

def fetch_projections(date: Optional[str] = None) -> Dict[str, Any]:
    """Fetch projections from SaberSim API."""
    config = load_config()
    token = config['token']
    slate_id = config['slate_id']
    cache_file = get_cache_file_path(date or datetime.now().strftime('%Y-%m-%d'))

    url = config['api_url']
    headers = {
        'authority': 'basketball-sim.appspot.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://sabersim.com',
        'referer': 'https://sabersim.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': random.choice(config['user_agents'])
    }
    data = {
        'date': date or datetime.now().strftime('%Y%m%d'),
        'sport': 'nba',
        'slate': slate_id,
        'percentile': '0',
        'site': 'fd',
        'conditionals': [],
        'version': '2.0'
    }

    try:
        response = make_api_request(url, headers, data)
        if not response:
            raise SSIMFetchError("No response received from API")
            
        json_data = handle_response(response)
        
        # Check if data has changed
        if has_data_changed(json_data, cache_file):
            # Update cache with new data and hash
            cache_data = {
                'hash': get_data_hash(json_data),
                'last_updated': datetime.now().strftime("%H:%M"),
                'players_count': len(json_data.get('players', []))
            }
            save_cache(cache_file, cache_data)
            logging.info(f"Found {cache_data['players_count']} new/updated projections")
            return json_data
        else:
            cached = load_cache(cache_file)
            logging.info(f"No changes since last update ({cached.get('players_count', 0)} players)")
            return json_data  # Return the data even if unchanged
            
    except SSIMFetchError as e:
        logging.error(f"Failed to fetch projections: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error fetching projections: {e}")
        raise SSIMFetchError(f"Unexpected error: {e}")

def validate_response(data: Dict[str, Any]) -> bool:
    """Validate API response data."""
    if not isinstance(data, dict):
        logging.error("Response is not a dictionary")
        return False
    
    required_fields = ['players']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logging.error(f"Missing required fields: {missing_fields}")
        return False
    
    if not isinstance(data['players'], list):
        logging.error("'players' field is not a list")
        return False
    
    if not data['players']:
        logging.error("'players' list is empty")
        return False
    
    # Validate player data structure
    required_player_fields = ['name', 'team', 'opp', 'minutes', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'three_pt_fg']
    for i, player in enumerate(data['players']):
        missing_player_fields = [field for field in required_player_fields if field not in player]
        if missing_player_fields:
            logging.error(f"Player {i} missing fields: {missing_player_fields}")
            return False
    
    return True

def save_raw_data(data: Dict[str, Any], date: str) -> Path:
    """Save raw projection data with metadata."""
    logger = logging.getLogger("ssim.fetch")
    
    # Standardize date format
    if date.lower() == 'today':
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Setup output directory - simplified path construction
    year_month = date[:7]  # YYYY-MM
    month_dir = DATA_ROOT / "nba/ssim/raw" / year_month
    month_dir.mkdir(parents=True, exist_ok=True)
    
    # Output file path
    json_file = month_dir / f"NBA_{date}_raw.json"
    
    # Add metadata
    data['metadata'] = {
        'fetch_timestamp': datetime.now().isoformat(),
        'num_players': len(data.get('players', [])),
        'version': '2.0',
        'source': 'sabersim',
        'sport': 'nba',
        'date': date
    }
    
    # Save data
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Saved {len(data.get('players', []))} players to {json_file}")
    return json_file

def setup_logging(level: str = "INFO") -> None:
    """Configure logging with color formatting."""
    logger = logging.getLogger("ssim.fetch")
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)

def fix_directory_structure() -> None:
    """Fix the directory structure by moving files to their correct locations."""
    logger = logging.getLogger("ssim.fetch")
    
    raw_dir = DATA_ROOT / "nba/ssim/raw"
    if not raw_dir.exists():
        logger.warning("Raw directory not found")
        return
        
    # Find all JSON files recursively
    json_files = list(raw_dir.rglob("NBA_*.json"))
    
    for file_path in json_files:
        try:
            # Extract date from filename (NBA_YYYY-MM-DD_raw.json)
            date_str = file_path.name.split("_")[1][:7]  # Gets YYYY-MM
            
            # Construct correct directory
            correct_dir = raw_dir / date_str
            correct_dir.mkdir(parents=True, exist_ok=True)
            
            # Construct correct path
            correct_path = correct_dir / file_path.name
            
            # Skip if file is already in correct location
            if file_path == correct_path:
                continue
                
            # Move file to correct location
            file_path.rename(correct_path)
            logger.info(f"Moved {file_path.name} to {correct_path}")
            
        except Exception as e:
            logger.error(f"Error moving {file_path}: {e}")
            continue
            
    logger.info("Directory structure cleanup complete")

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Fetch SaberSim NBA projections')
    parser.add_argument('--date', default='today', help='Date to fetch (YYYY-MM-DD or "today")')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      help='Logging level')
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    logger = logging.getLogger("ssim.fetch")
    
    try:
        logger.info(f"Fetching projections for {args.date}")
        data = fetch_projections(args.date)
        save_raw_data(data, args.date)
        fix_directory_structure()
        logger.info("✓ Fetch completed successfully")
        return 0
        
    except SSIMAuthError as e:
        logger.error(f"Authentication error: {e}")
        return 1
    except SSIMRateLimitError as e:
        logger.error(f"Rate limit error: {e}")
        return 1
    except SSIMDataError as e:
        logger.error(f"Data validation error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 