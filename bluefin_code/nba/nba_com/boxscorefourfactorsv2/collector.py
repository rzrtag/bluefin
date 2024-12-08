#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
from nba_api.stats.endpoints import boxscorefourfactorsv2

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "boxscorefourfactorsv2"
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

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

def get_four_factors_stats(game_id: str, date: str, force_fresh: bool = False) -> Optional[pd.DataFrame]:
    """Get four factors stats for a game from NBA.com."""
    print(f"\nFetching four factors stats for game {game_id}")
    
    # Get year-month for organization
    year_month = get_year_month(date)
    
    # Create cache path
    cache_dir = RAW_DIR / year_month
    cache_path = cache_dir / f"{game_id}.csv"
    
    # Return cached data if it exists and we're not forcing fresh
    if not force_fresh and cache_path.exists():
        print(f"Using cached data from {cache_path}")
        return pd.read_csv(cache_path)
    
    # Ensure cache directory exists
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        print("Fetching data from NBA API...")
        # Get data from NBA API
        boxscore = boxscorefourfactorsv2.BoxScoreFourFactorsV2(
            game_id=game_id,
            start_period='0',  # API expects strings
            end_period='10',
            start_range='0',
            end_range='28800',
            range_type='0'
        )
        
        # Convert to DataFrame
        df = boxscore.get_data_frames()[0]
        print(f"Got data with {len(df)} rows")
        
        # Cache the raw data
        df.to_csv(cache_path, index=False)
        print(f"Cached raw data to {cache_path}")
        
        return df
        
    except Exception as e:
        print(f"Error getting data for game {game_id}: {str(e)}")
        return None

def process_four_factors_stats(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Process raw four factors stats into clean format."""
    if df is None or len(df) == 0:
        return None
        
    # Select and rename columns we want
    cols = {
        'GAME_ID': 'game_id',
        'TEAM_ID': 'team_id',
        'TEAM_ABBREVIATION': 'team',
        'PLAYER_ID': 'player_id',
        'PLAYER_NAME': 'player',
        'START_POSITION': 'start_position',
        'COMMENT': 'status',
        'MIN': 'minutes',
        'EFG_PCT': 'effective_fg_pct',
        'FTA_RATE': 'free_throw_rate',
        'TM_TOV_PCT': 'turnover_pct',
        'OREB_PCT': 'offensive_rebound_pct',
        'OPP_EFG_PCT': 'opp_effective_fg_pct',
        'OPP_FTA_RATE': 'opp_free_throw_rate',
        'OPP_TOV_PCT': 'opp_turnover_pct',
        'OPP_OREB_PCT': 'opp_offensive_rebound_pct'
    }
    
    # Select and rename columns
    df = df[cols.keys()].rename(columns=cols)
    
    # Convert minutes to float
    def convert_minutes(x) -> float:
        if pd.isna(x) or not str(x).strip():
            return 0.0
        x_str = str(x).strip()
        if ':' in x_str:
            try:
                minutes, seconds = x_str.split(':')
                return float(minutes) + float(seconds)/60
            except (ValueError, IndexError):
                print(f"Warning: Could not parse minutes value: {x_str}")
                return 0.0
        try:
            return float(x_str)
        except ValueError:
            print(f"Warning: Could not convert minutes value to float: {x_str}")
            return 0.0
    
    df['minutes'] = df['minutes'].apply(convert_minutes)
    
    # Convert percentage columns to actual percentages
    pct_cols = [col for col in df.columns if 'pct' in col.lower()]
    for col in pct_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) / 100
    
    # Print some debug info
    print(f"\nProcessed {len(df)} rows of four factors stats")
    print(f"Players with minutes > 0: {len(df[df['minutes'] > 0])}")
    
    return df

def save_four_factors_stats(game_id: str, date: str, force_fresh: bool = False) -> None:
    """Get and save four factors stats for a game."""
    print(f"\nProcessing game {game_id} from {date}")
    
    # Get raw data
    raw_df = get_four_factors_stats(game_id, date, force_fresh)
    if raw_df is None:
        print("Failed to get raw data")
        return
    
    # Process data
    df = process_four_factors_stats(raw_df)
    if df is None:
        print("Failed to process data")
        return
    
    # Get year-month
    year_month = get_year_month(date)
    save_dir = PROCESSED_DIR / year_month
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save processed data
    save_path = save_dir / f"four_factors_{game_id}.csv"
    df.to_csv(save_path, index=False)
    print(f"Saved processed data to {save_path}")

def main():
    """Example usage."""
    print("\nNBA Four Factors Stats Collector")
    print("------------------------------")
    
    # Example games from different parts of season
    test_games = [
        ("0022400001", "2024-10-24"),  # October 2024
        ("0022400234", "2024-12-06"),  # December 2024
        ("0022400456", "2025-01-15"),  # January 2025
    ]
    
    for game_id, date in test_games:
        print(f"\nCollecting data for:")
        print(f"Game ID: {game_id}")
        print(f"Date: {date}")
        year_month = get_year_month(date)
        print(f"Year-Month: {year_month}")
        
        # Get and save stats
        save_four_factors_stats(game_id, date, force_fresh=True)  # Force fresh data for testing

if __name__ == "__main__":
    main() 