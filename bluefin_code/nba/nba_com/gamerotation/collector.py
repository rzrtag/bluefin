#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from nba_api.stats.endpoints import gamerotation
import time

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "gamerotation"
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

# API rate limiting - Extremely aggressive settings for full collection
RATE_LIMIT_CALLS = 240  # 4 calls per second
RATE_LIMIT_PERIOD = 60  # Period in seconds
MIN_CALL_GAP = 0.25  # Quarter second between calls

def get_year_month(date: str) -> str:
    """
    Get year-month string from date.
    
    Args:
        date: Date string in YYYY-MM-DD format
    
    Returns:
        Year-month string like "2024-12"
    """
    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt.strftime("%Y-%m")

def get_rotation_stats(game_id: str, date: str, force_fresh: bool = False) -> Optional[Dict[str, pd.DataFrame]]:
    """Get rotation stats for a game from NBA.com."""
    # Ensure game_id is a string
    game_id = str(game_id)
    
    print(f"\nFetching rotation stats for game {game_id}")
    
    # Get year-month for organization
    year_month = get_year_month(date)
    
    # Create cache path
    cache_dir = RAW_DIR / year_month
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Cache paths for each result set
    cache_paths = {
        'home': cache_dir / f"{game_id}_home.csv",
        'away': cache_dir / f"{game_id}_away.csv"
    }
    
    # Return cached data if it exists and we're not forcing fresh
    if not force_fresh and all(p.exists() for p in cache_paths.values()):
        print(f"Using cached data from {cache_dir}")
        return {
            'home': pd.read_csv(cache_paths['home']),
            'away': pd.read_csv(cache_paths['away'])
        }
    
    try:
        print("Fetching data from NBA API...")
        # Get data from NBA API - game_id should be string like "0022300001"
        if not str(game_id).startswith('00'):
            game_id = f"00{game_id}"
            
        rotation = gamerotation.GameRotation(game_id=game_id)
        
        # Get all result sets
        all_dfs = rotation.get_data_frames()
        
        if not all_dfs or len(all_dfs) < 2:
            print("No data returned from API")
            return None
            
        # Get relevant result sets
        home_rotation = all_dfs[0]  # HomeTeam
        away_rotation = all_dfs[1]  # AwayTeam
        
        # Cache the raw data
        home_rotation.to_csv(cache_paths['home'], index=False)
        away_rotation.to_csv(cache_paths['away'], index=False)
        print(f"Cached raw data to {cache_dir}")
        
        # Brief pause to respect rate limit
        time.sleep(MIN_CALL_GAP)
        
        return {
            'home': home_rotation,
            'away': away_rotation
        }
        
    except Exception as e:
        print(f"Error getting data for game {game_id}: {str(e)}")
        time.sleep(MIN_CALL_GAP)  # Brief pause on error
        return None

def process_rotation_stats(data: Optional[Dict[str, pd.DataFrame]]) -> Optional[pd.DataFrame]:
    """Process raw rotation stats into clean format."""
    if data is None:
        return None
        
    home_rotation = data['home'].copy()  # Make copies to avoid SettingWithCopyWarning
    away_rotation = data['away'].copy()
    
    # Process rotations
    rotation_cols = {
        'GAME_ID': 'game_id',
        'TEAM_ID': 'team_id',
        'TEAM_CITY': 'team_city',
        'TEAM_NAME': 'team_name',
        'PERSON_ID': 'player_id',
        'PLAYER_NAME': 'player',
        'IN_TIME_REAL': 'in_time',
        'OUT_TIME_REAL': 'out_time',
        'ELAPSED_TIME_REAL': 'elapsed_time',
        'PERIOD': 'quarter',
        'SEQUENCE': 'sequence'
    }
    
    # Only select columns that exist
    available_cols = [col for col in rotation_cols.keys() if col in home_rotation.columns]
    
    # Process each rotation DataFrame
    home_rotation = home_rotation[available_cols].rename(columns={col: rotation_cols[col] for col in available_cols})
    away_rotation = away_rotation[available_cols].rename(columns={col: rotation_cols[col] for col in available_cols})
    
    # Add team identifier BEFORE concat
    home_rotation.loc[:, 'is_home'] = True
    away_rotation.loc[:, 'is_home'] = False
    
    # Combine rotations
    df = pd.concat([home_rotation, away_rotation], ignore_index=True)
    
    # Convert time columns to datetime
    time_cols = ['in_time', 'out_time']
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    # Convert elapsed time to seconds
    if 'elapsed_time' in df.columns:
        def convert_elapsed_time(x) -> float:
            if pd.isna(x) or not str(x).strip():
                return 0.0
            x_str = str(x).strip()
            if ':' in x_str:
                try:
                    minutes, seconds = x_str.split(':')
                    return float(minutes) * 60 + float(seconds)
                except (ValueError, IndexError):
                    print(f"Warning: Could not parse elapsed time value: {x_str}")
                    return 0.0
            try:
                return float(x_str)
            except ValueError:
                print(f"Warning: Could not convert elapsed time value to float: {x_str}")
                return 0.0
        
        df['elapsed_time'] = df['elapsed_time'].apply(convert_elapsed_time)
    
    # Sort by sequence
    if 'sequence' in df.columns:
        df = df.sort_values(['quarter', 'sequence'])
    
    # Print some debug info
    print(f"\nProcessed {len(df)} rotation records")
    print(f"Home team records: {len(df[df['is_home']])}")
    print(f"Away team records: {len(df[~df['is_home']])}")
    
    return df

def save_rotation_stats(game_id: str, date: str, force_fresh: bool = False) -> None:
    """Get and save rotation stats for a game."""
    print(f"\nProcessing game {game_id} from {date}")
    
    # Get raw data
    raw_data = get_rotation_stats(game_id, date, force_fresh)
    if raw_data is None:
        print("Failed to get raw data")
        return
    
    # Process data
    df = process_rotation_stats(raw_data)
    if df is None:
        print("Failed to process data")
        return
    
    # Get year-month
    year_month = get_year_month(date)
    save_dir = PROCESSED_DIR / year_month
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save processed data
    save_path = save_dir / f"rotation_{game_id}.csv"
    df.to_csv(save_path, index=False)
    print(f"Saved processed data to {save_dir}")

def main():
    """Example usage."""
    print("\nNBA Rotation Stats Collector")
    print("-------------------------")
    
    # Test with a known game ID
    test_game = ("0022300001", "2023-10-24")  # First game of 2023-24 season
    save_rotation_stats(test_game[0], test_game[1], force_fresh=True)

if __name__ == "__main__":
    main()