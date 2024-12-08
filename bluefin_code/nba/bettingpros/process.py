#!/usr/bin/env python3

import json
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional, Set, Any
import sys
import argparse
from os.path import dirname, abspath

# Add parent directory to path
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))

from bluefin_code.nba.utils import BOOKS_CONFIG, MARKETS_CONFIG
from bluefin_code.core.output import print_header, print_section, print_subsection, print_warning, format_change, format_player_update

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_data_dir(date: str) -> Path:
    """Get data directory for a given date."""
    month = date[:7]  # YYYY-MM
    return Path('/home/rzrtag/work/bluefin/bluefin_data/nba/bettingpros/raw') / month

def get_output_dir(date: str) -> Path:
    """Get output directory for a given date."""
    month = date[:7]  # YYYY-MM
    return Path('/home/rzrtag/work/bluefin/bluefin_data/nba/bettingpros/processed') / month

def load_events(date: str) -> Dict:
    """Load events data for a given date."""
    data_dir = get_data_dir(date)
    events_file = data_dir / f"{date}_events.json"
    
    if not events_file.exists():
        logger.error(f"Events file not found: {events_file}")
        return {}
        
    try:
        with open(events_file) as f:
            events_data = json.load(f)
            
        # Create a mapping of team abbreviations to game info
        games = {}
        for event in events_data.get('events', []):
            home_team = event.get('home')
            away_team = event.get('visitor')
            if home_team and away_team:
                games[home_team] = {
                    'opponent': away_team,
                    'is_home': True,
                    'scheduled': event.get('scheduled')
                }
                games[away_team] = {
                    'opponent': home_team,
                    'is_home': False,
                    'scheduled': event.get('scheduled')
                }
                
        logger.info(f"Loaded {len(games)//2} games for {date}")
        return games
        
    except Exception as e:
        logger.error(f"Error loading events: {str(e)}")
        return {}

def load_book_data(date: str, book_abbrev: str) -> Optional[Dict]:
    """Load sportsbook data for a given date."""
    data_dir = get_data_dir(date)
    book_file = data_dir / f"{date}_{book_abbrev}.json"
    
    if not book_file.exists():
        logger.warning(f"Book file not found: {book_file}")
        return None
        
    try:
        with open(book_file) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading book data: {str(e)}")
        return None

def get_market_name(market_id: int) -> str:
    """Get standardized market name from market ID."""
    for market in MARKETS_CONFIG['markets'].values():
        if market['market_id'] == str(market_id):
            return market['abbreviation']
    return 'unknown'

def is_valid_line(market_name: str, line: float) -> bool:
    """Validate if a betting line is reasonable for the given market."""
    try:
        # Convert line to float for validation
        line = float(line)
        
        # Market-specific validation
        if market_name == 'BLK':
            return 0 <= line <= 5  # Very rare to see block props over 5
        elif market_name == 'TO':
            return 0 <= line <= 8  # Very rare to see turnover props over 8
        elif market_name in ['3PM', 'THREESM']:
            return 0 <= line <= 8  # Very rare to see 3PM props over 8
        elif market_name == 'PTS':
            return 0 <= line <= 50  # Very rare to see point props over 50
        elif market_name == 'REB':
            return 0 <= line <= 20  # Very rare to see rebound props over 20
        elif market_name == 'AST':
            return 0 <= line <= 15  # Very rare to see assist props over 15
        elif market_name == 'STL':
            return 0 <= line <= 5  # Very rare to see steal props over 5
        elif market_name == 'PRA':
            return 0 <= line <= 75  # Very rare to see PRA props over 75
        elif market_name in ['PA', 'PR']:
            return 0 <= line <= 60  # Very rare to see PA/PR props over 60
        return True  # Allow other markets through
    except (TypeError, ValueError):
        return False

def process_book_data(date: str, book_abbrev: str, games: Dict) -> List[Dict]:
    """Process sportsbook data for a given date."""
    records = []
    data = load_book_data(date, book_abbrev)
    
    if not data:
        return records
        
    try:
        # Extract props from data
        props = data.get('props', [])
        logger.info(f"Found {len(props)} props for {book_abbrev}")
        
        for prop in props:
            try:
                # Extract participant info
                participant = prop.get('participant', {})
                player = participant.get('player', {})
                player_name = f"{player.get('first_name', '')} {player.get('last_name', '')}".strip()
                team = player.get('team', '')
                
                if not player_name or not team:
                    continue
                    
                game_info = games.get(team)
                if not game_info:
                    logger.warning(f"No game found for team {team}")
                    continue
                    
                # Extract market info
                market_id = prop.get('market_id')
                market_name = get_market_name(market_id)
                
                # Extract odds info
                over = prop.get('over', {})
                under = prop.get('under', {})
                line = over.get('line')
                over_odds = over.get('odds')
                under_odds = under.get('odds')
                
                if not all([market_name, line is not None, over_odds is not None, under_odds is not None]):
                    continue
                    
                # Validate line
                if not is_valid_line(market_name, line):
                    logger.warning(f"Invalid line for {player_name} {market_name}: {line}")
                    continue
                    
                records.append({
                    'date': date,
                    'player': player_name,
                    'team': team,
                    'opponent': game_info['opponent'],
                    'is_home': game_info['is_home'],
                    'scheduled': game_info['scheduled'],
                    'market': market_name,
                    'line': line,
                    'over_odds': over_odds,
                    'under_odds': under_odds,
                    'book': BOOKS_CONFIG['sportsbooks'][book_abbrev]['display_name']
                })
                
            except Exception as e:
                logger.warning(f"Error processing prop: {str(e)}")
                continue
                
        logger.info(f"Processed {len(records)} props for {book_abbrev}")
                
    except Exception as e:
        logger.error(f"Error processing book data: {str(e)}")
        logger.debug(f"Raw data: {data}")
        
    return records

def process_date(date: str) -> None:
    """Process all sportsbook data for a given date."""
    print_header(f"Processing data for {date}")
    
    # Load events first
    games = load_events(date)
    if not games:
        print_warning(f"No games found for {date}")
        return
        
    # Process each sportsbook
    all_records = []
    for book_abbrev, book_info in BOOKS_CONFIG['sportsbooks'].items():
        print_section(f"Processing {book_info['name']}")
        records = process_book_data(date, book_abbrev, games)
        all_records.extend(records)
        print_subsection(f"Found {len(records)} records")
    
    if not all_records:
        print_warning("No records found")
        return
        
    # Create output directory
    output_dir = get_output_dir(date)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df = pd.DataFrame(all_records)
    output_file = output_dir / f"{date}.csv"
    df.to_csv(output_file, index=False)
    print_section(f"Saved {len(df)} records to {output_file}")

def process_data(data: List[Dict[str, Any]], old_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Process raw data and show changes."""
    processed = []
    
    if old_data is not None:
        old_lines = {
            (row['player'], row['market'], row['book']): row 
            for _, row in old_data.iterrows()
        }
        
        for prop in data:
            key = (prop['player'], prop['market'], prop['book'])
            if key in old_lines:
                old = old_lines[key]
                updates = {}
                
                if abs(prop['line'] - old['line']) > 0.1:
                    updates['line'] = (old['line'], prop['line'])
                if prop['over_odds'] != old['over_odds']:
                    updates['over_odds'] = (old['over_odds'], prop['over_odds'])
                    
                if updates:
                    print(format_player_update(f"{prop['player']} ({prop['market']} {prop['book']})", updates))
                    
    return pd.DataFrame(processed)

def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='Date to process (YYYY-MM-DD)', default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    
    process_date(args.date)

if __name__ == '__main__':
    main()