#!/usr/bin/env python3

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import hashlib
import pandas as pd
from bluefin_code.core.output import format_change, format_player_update
from colorama import Fore, Style

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"

def get_raw_file_path(date: str) -> Path:
    """Get path to raw data file."""
    year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
    return DATA_ROOT / "nba" / "ssim" / "raw" / year_month / f"NBA_{date}_raw.json"

def get_processed_file_path(date: str) -> Path:
    """Get path to processed data file."""
    year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
    return DATA_ROOT / "nba" / "ssim" / "processed" / year_month / f"ssim_{date}.csv"

def load_raw_data(date: str) -> Dict[str, Any]:
    """Load raw data for a given date."""
    raw_file = get_raw_file_path(date)
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw data file not found: {raw_file}")
        
    with open(raw_file) as f:
        return json.load(f)

def process_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process raw data into standardized format."""
    processed_players = []
    for player in data['players']:
        try:
            # Flatten nested structures
            processed_player = {
                'date': data.get('metadata', {}).get('date'),
                'name': player.get('name'),
                'team': player.get('team'),
                'opponent': player.get('opp'),
                'minutes': player.get('minutes'),
                'points': player.get('points'),
                'rebounds': player.get('rebounds'),
                'assists': player.get('assists'),
                'steals': player.get('steals'),
                'blocks': player.get('blocks'),
                'turnovers': player.get('turnovers'),
                'three_pt_fg': player.get('three_pt_fg'),
                'three_pt_attempts': player.get('three_pt_attempts'),
                'two_pt_fg': player.get('two_pt_fg'),
                'two_pt_attempts': player.get('two_pt_attempts'),
                'free_throws_made': player.get('free_throws_made'),
                'free_throw_attempts': player.get('free_throw_attempts'),
                'offensive_rebounds': player.get('offensive_rebounds'),
                'defensive_rebounds': player.get('defensive_rebounds'),
                'fouls': player.get('fouls'),
                
                # Fantasy Points - DK only
                'dk_points': player.get('dk_points'),
                'dk_std': player.get('dk_std'),
                
                # DK Percentiles
                'dk_25_percentile': player.get('dk_25_percentile'),
                'dk_50_percentile': player.get('dk_50_percentile'),
                'dk_75_percentile': player.get('dk_75_percentile'),
                'dk_85_percentile': player.get('dk_85_percentile'),
                'dk_95_percentile': player.get('dk_95_percentile'),
                'dk_99_percentile': player.get('dk_99_percentile'),
                
                # Additional Fields
                'price': player.get('price'),
                'value': player.get('value'),
                'proj_own': player.get('proj_own', 0),
                'position': player.get('position'),
                'roster_pos': player.get('roster_pos'),
                'injury': player.get('injury'),
                'injury_notes': player.get('injury_notes'),
                'injury_confirmed': player.get('injury_confirmed'),
                'confirmed': player.get('confirmed'),
                'site': player.get('site'),
                'slate': player.get('slate'),
                'gid': player.get('gid'),
                'pid': player.get('pid'),
                'num_games': player.get('num_games'),
                'possessions': player.get('possessions'),
                'double_doubles': player.get('double_doubles'),
                'triple_doubles': player.get('triple_doubles'),
                
                'timestamp': data.get('timestamp'),
                
                # Calculated aggregated markets
                'points_rebounds': player.get('points', 0) + player.get('rebounds', 0),
                'points_assists': player.get('points', 0) + player.get('assists', 0),
                'rebounds_assists': player.get('rebounds', 0) + player.get('assists', 0),
                'points_rebounds_assists': player.get('points', 0) + player.get('rebounds', 0) + player.get('assists', 0),
                'stocks': player.get('steals', 0) + player.get('blocks', 0),
            }
            processed_players.append(processed_player)
        except KeyError as e:
            logging.error(f"Missing required field {e} for player {player.get('name', 'UNKNOWN')}")
            raise
        except Exception as e:
            logging.error(f"Failed to process player {player.get('name', 'UNKNOWN')}: {e}")
            raise
    
    return processed_players

def process_date(date: str, force: bool = False) -> None:
    """Process data for a specific date."""
    logger = logging.getLogger("ssim.process")
    
    try:
        # Load and process raw data
        logger.info(f"\n{Fore.CYAN}Processing SaberSim data for {date}{Style.RESET_ALL}")
        
        # Load previous data if exists
        output_file = get_processed_file_path(date)
        old_data = {}
        if output_file.exists():
            old_df = pd.read_csv(output_file)
            old_data = {row['name']: row for _, row in old_df.iterrows()}
        
        # Process new data
        raw_data = load_raw_data(date)
        processed_data = process_data(raw_data)
        
        # Track and display changes
        for player in processed_data:
            name = player['name']
            if name in old_data:
                updates = {}
                old = old_data[name]
                if abs(player['minutes'] - old['minutes']) > 0.1:
                    updates['minutes'] = (old['minutes'], player['minutes'])
                
                if updates:
                    print(format_player_update(name, updates))
        
        # Save processed data
        df = pd.DataFrame(processed_data)
        df.to_csv(output_file, index=False)
            
        logger.info(f"✓ Processed {len(processed_data)} players")
        
    except Exception as e:
        logger.error(f"Failed to process {date}: {e}")
        raise

def process_all_raw_files(force: bool = False) -> None:
    """Process all raw files that haven't been processed yet."""
    logger = logging.getLogger("ssim.process")
    
    raw_dir = DATA_ROOT / "nba/ssim/raw"
    if not raw_dir.exists():
        logger.error("Raw directory not found")
        return
        
    # Find all raw JSON files
    raw_files = []
    for month_dir in raw_dir.iterdir():
        if month_dir.is_dir():
            raw_files.extend(month_dir.glob("NBA_*_raw.json"))
    
    logger.info(f"Found {len(raw_files)} raw files")
    
    for raw_file in sorted(raw_files):
        try:
            # Extract date from filename (NBA_YYYY-MM-DD_raw.json)
            date_str = raw_file.name.split("_")[1]
            
            # Process this date
            process_date(date_str, force)
            
        except Exception as e:
            logger.error(f"Error processing {raw_file.name}: {e}")
            continue
            
    logger.info("Batch processing complete")

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Process SaberSim NBA data")
    parser.add_argument("--date", help="Date to process (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--force", action="store_true", help="Force reprocess existing files")
    parser.add_argument("--all", action="store_true", help="Process all raw files")
    args = parser.parse_args()

    try:
        if args.all:
            process_all_raw_files(args.force)
        else:
            process_date(args.date, args.force)
        return 0

    except Exception as e:
        logging.error(f"Failed to process: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())