#!/usr/bin/env python3

import argparse
from pathlib import Path
import json
import logging
import time
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional, NamedTuple
import pandas as pd
from dataclasses import dataclass
import sys
from os.path import dirname, abspath

# Add parent directory to path
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))

from bluefin_code.nba.utils import MARKETS_CONFIG, BOOKS_CONFIG
from bluefin_code.core.output import print_header, print_section, print_subsection, print_warning

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@dataclass
class Sportsbook:
    name: str
    abbreviation: str
    url: str

@dataclass
class Config:
    sportsbooks: List[Sportsbook]
    headers: Dict[str, str]
    base_url: str

def create_default_config() -> Config:
    """Create default configuration."""
    sportsbooks = [
        Sportsbook(name="DraftKings", abbreviation="dk", url="draftkings"),
        Sportsbook(name="FanDuel", abbreviation="fd", url="fanduel"),
        Sportsbook(name="BetMGM", abbreviation="mgm", url="betmgm"),
        Sportsbook(name="ESPN BET", abbreviation="espn", url="espn-bet"),
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.bettingpros.com/',
        'Origin': 'https://www.bettingpros.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    base_url = "https://api.bettingpros.com/v3/props"
    
    return Config(sportsbooks=sportsbooks, headers=headers, base_url=base_url)

def get_data_dir(date: str) -> Path:
    """Get data directory for a given date."""
    month = date[:7]  # YYYY-MM
    return Path('/home/rzrtag/work/bluefin/bluefin_data/nba/bettingpros/raw') / month

def fetch_sportsbook_data(book: Sportsbook, date: str, config: Config, force: bool = False) -> tuple[Optional[Path], Dict]:
    """Fetch data for a specific sportsbook."""
    output_dir = get_data_dir(date)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{date}_{book.abbreviation}.json"
    
    # Skip if file exists and not forcing
    if output_file.exists() and not force:
        logger.info(f"Skipping {book.name} - file exists")
        return None, {}
        
    # Construct params
    params = {
        'sport': 'NBA',
        'date': date,
        'book_id': BOOKS_CONFIG['sportsbooks'][book.abbreviation]['book_id'],
        'market_id': ','.join(m['market_id'] for m in MARKETS_CONFIG['markets'].values()),
        'include_markets': 'true',
        'include_events': 'true',
        'limit': '9999'
    }
    
    try:
        # Make request
        response = requests.get(config.base_url, headers=config.headers, params=params)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(data, f)
            
        logger.info(f"Fetched {book.name} data")
        
        return output_file, {
            'status': 'success',
            'size': len(response.content)
        }
        
    except Exception as e:
        logger.error(f"Error fetching {book.name}: {str(e)}")
        return None, {
            'status': 'error',
            'error': str(e)
        }

def fetch_events(date: str, config: Config, force: bool = False) -> Optional[Path]:
    """Fetch events data."""
    output_dir = get_data_dir(date)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{date}_events.json"
    
    # Skip if file exists and not forcing
    if output_file.exists() and not force:
        logger.info(f"Skipping events - file exists")
        return None
        
    # Construct params
    params = {
        'sport': 'NBA',
        'date': date,
        'include_events': 'true',
        'include_lineups': 'true',
        'include_markets': 'false',
        'limit': '1'  # We only need events data
    }
    
    try:
        # Make request
        response = requests.get(
            config.base_url,  # Use the same base URL as props
            headers=config.headers,
            params=params
        )
        response.raise_for_status()
        
        # Parse response and extract events
        data = response.json()
        events_data = {'events': data.get('events', [])}
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(events_data, f)
            
        logger.info(f"Fetched events data")
        return output_file
        
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        return None

def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='Date to fetch (YYYY-MM-DD)', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--force', action='store_true', help='Force fetch new data')
    args = parser.parse_args()
    
    config = create_default_config()
    
    # Fetch events first
    events_file = fetch_events(args.date, config, force=args.force)
    
    # Fetch each sportsbook
    for book in config.sportsbooks:
        fetch_sportsbook_data(book, args.date, config, force=args.force)
        time.sleep(1)  # Be nice to the API

if __name__ == '__main__':
    main()