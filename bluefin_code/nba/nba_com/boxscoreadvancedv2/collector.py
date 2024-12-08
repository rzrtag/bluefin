#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
from nba_api.stats.endpoints import boxscoreadvancedv2

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "boxscoreadvancedv2"
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

def get_advanced_stats(game_id: str, date: str, force_fresh: bool = False) -> Optional[pd.DataFrame]:
    """Get advanced stats for a game from NBA.com."""
    # Ensure game_id is a string and properly formatted
    game_id = str(game_id)
    if len(game_id) == 10:  # Already full format (0022300001)
        api_game_id = game_id
    elif len(game_id) == 8:  # Short format (22300001)
        api_game_id = f"00{game_id}"
    else:
        print(f"Invalid game ID format: {game_id}")
        return None
    
    print(f"\nFetching advanced stats for game {game_id}")
    
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
        boxscore = boxscoreadvancedv2.BoxScoreAdvancedV2(
            game_id=api_game_id,
            start_period="0",
            end_period="10",
            start_range="0",
            end_range="28800",
            range_type="0"
        )
        
        # Get all result sets
        all_dfs = boxscore.get_data_frames()
        
        if not all_dfs or len(all_dfs) == 0:
            print("No data returned from API")
            return None
            
        # Get player stats
        df = all_dfs[0]  # First result set is player stats
        print(f"Got data with {len(df)} rows")
        
        # Cache the raw data
        df.to_csv(cache_path, index=False)
        print(f"Cached raw data to {cache_path}")
        
        return df
        
    except Exception as e:
        print(f"Error getting data for game {game_id}: {str(e)}")
        return None

def process_advanced_stats(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Process raw advanced stats into clean format."""
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
        'E_OFF_RATING': 'offensive_rating',
        'E_DEF_RATING': 'defensive_rating',
        'E_NET_RATING': 'net_rating',
        'AST_PCT': 'assist_pct',
        'AST_TOV': 'assist_to_turnover',
        'AST_RATIO': 'assist_ratio',
        'OREB_PCT': 'offensive_rebound_pct',
        'DREB_PCT': 'defensive_rebound_pct',
        'REB_PCT': 'rebound_pct',
        'TM_TOV_PCT': 'turnover_pct',
        'EFG_PCT': 'effective_fg_pct',
        'TS_PCT': 'true_shooting_pct',
        'USG_PCT': 'usage_pct',
        'E_USG_PCT': 'usage_pct_excluding_tm_plays',
        'E_PACE': 'pace',
        'PACE_PER40': 'pace_per_40',
        'POSS': 'possessions',
        'PIE': 'player_impact_estimate'
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
    
    # Convert IDs to string and remove leading zeros from game_id
    df['game_id'] = df['game_id'].astype(str).str.lstrip('0')
    df['team_id'] = df['team_id'].astype(str)
    df['player_id'] = df['player_id'].astype(str).str.lstrip('0')  # Remove leading zeros from player_id
    
    # Print some debug info
    print(f"\nProcessed {len(df)} rows of advanced stats")
    print(f"Players with minutes > 0: {len(df[df['minutes'] > 0])}")
    
    return df

def save_advanced_stats(game_id: str, date: str, force_fresh: bool = False) -> None:
    """Get and save advanced stats for a game."""
    print(f"\nProcessing game {game_id} from {date}")
    
    # Get raw data
    raw_df = get_advanced_stats(game_id, date, force_fresh)
    if raw_df is None:
        print("Failed to get raw data")
        return
    
    # Process data
    df = process_advanced_stats(raw_df)
    if df is None:
        print("Failed to process data")
        return
    
    # Get year-month
    year_month = get_year_month(date)
    save_dir = PROCESSED_DIR / year_month
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save processed data
    save_path = save_dir / f"advanced_{game_id}.csv"
    df.to_csv(save_path, index=False)
    print(f"Saved processed data to {save_path}")

def get_player_ids_from_game(game_id: str, date: str) -> list[str]:
    """Extract unique player IDs from a game's advanced stats."""
    df = get_advanced_stats(game_id, date)
    if df is None:
        return []
    
    # Get unique player IDs and ensure they're strings
    player_ids = df['PLAYER_ID'].unique().astype(str).tolist()
    print(f"Found {len(player_ids)} unique players in game {game_id}")
    return player_ids

def main():
    """Example usage."""
    print("\nNBA Advanced Stats Collector")
    print("---------------------------")
    
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
        
        # Get and save stats
        save_advanced_stats(game_id, date, force_fresh=True)
        
        # Extract player IDs
        player_ids = get_player_ids_from_game(game_id, date)
        print(f"Player IDs from game: {player_ids}")

if __name__ == "__main__":
    main() 