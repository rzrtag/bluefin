#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
from nba_api.stats.endpoints import playergamelog

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "playergamelog"
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

def get_player_gamelog(player_id: str, season: str = "2024-25", force_fresh: bool = False) -> Optional[pd.DataFrame]:
    """Get game log for a player from NBA.com."""
    # Ensure player_id is a string
    player_id = str(player_id)
    
    print(f"\nFetching game log for player {player_id}")
    
    # Create cache path using season
    cache_dir = RAW_DIR / season
    cache_path = cache_dir / f"{player_id}_{season}.csv"
    
    # Return cached data if it exists and we're not forcing fresh
    if not force_fresh and cache_path.exists():
        print(f"Using cached data from {cache_path}")
        return pd.read_csv(cache_path)
    
    # Ensure cache directory exists
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        print("Fetching data from NBA API...")
        # Get data from NBA API
        gamelog = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season,
            season_type_all_star="Regular Season"
        )
        
        # Get all result sets
        all_dfs = gamelog.get_data_frames()
        
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
        print(f"Error getting data for player {player_id}: {str(e)}")
        return None

def process_gamelog(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Process raw game log into clean format."""
    if df is None or len(df) == 0:
        return None
        
    try:
        # Select and rename columns we want
        cols = {
            'Game_ID': 'game_id',
            'GAME_DATE': 'game_date',
            'MATCHUP': 'matchup',
            'WL': 'win_loss',
            'MIN': 'minutes',
            'FGM': 'field_goals_made',
            'FGA': 'field_goals_attempted',
            'FG_PCT': 'field_goal_pct',
            'FG3M': 'three_pointers_made',
            'FG3A': 'three_pointers_attempted',
            'FG3_PCT': 'three_point_pct',
            'FTM': 'free_throws_made',
            'FTA': 'free_throws_attempted',
            'FT_PCT': 'free_throw_pct',
            'OREB': 'offensive_rebounds',
            'DREB': 'defensive_rebounds',
            'REB': 'rebounds',
            'AST': 'assists',
            'STL': 'steals',
            'BLK': 'blocks',
            'TOV': 'turnovers',
            'PF': 'personal_fouls',
            'PTS': 'points',
            'PLUS_MINUS': 'plus_minus'
        }
        
        # Print available columns for debugging
        print("\nAvailable columns:", df.columns.tolist())
        
        # Select and rename columns that exist
        available_cols = [col for col in cols.keys() if col in df.columns]
        df = df[available_cols].rename(columns={col: cols[col] for col in available_cols})
        
        # Convert game date to YYYY-MM-DD format
        # NBA API returns dates like "OCT 24, 2023" - specify format
        df['game_date'] = pd.to_datetime(df['game_date'], format='%b %d, %Y').dt.strftime('%Y-%m-%d')
        
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
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Print some debug info
        print(f"\nProcessed {len(df)} rows of game log data")
        print(f"Games with minutes > 0: {len(df[df['minutes'] > 0])}")
        
        return df
        
    except Exception as e:
        print(f"Error processing game log: {str(e)}")
        print("DataFrame head:")
        print(df.head())
        return None

def save_player_gamelog(player_id: str, season: str = "2024-25", force_fresh: bool = False) -> None:
    """Get and save game log for a player."""
    # Get raw data
    raw_df = get_player_gamelog(player_id, season, force_fresh)
    if raw_df is None:
        print("Failed to get raw data")
        return
    
    # Process data
    df = process_gamelog(raw_df)
    if df is None:
        print("Failed to process data")
        return
    
    # Save to season directory
    save_dir = PROCESSED_DIR / season
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save processed data
    save_path = save_dir / f"gamelog_{player_id}_{season}.csv"
    df.to_csv(save_path, index=False)
    print(f"Saved processed data to {save_path}")

def main():
    """Example usage."""
    print("\nNBA Player Game Log Collector")
    print("----------------------------")
    
    # Example players
    test_players = [
        "2544",  # LeBron James
        "203999",  # Nikola Jokic
        "1629029",  # Luka Doncic
    ]
    
    for player_id in test_players:
        print(f"\nCollecting data for player {player_id}")
        
        # Get and save game log
        save_player_gamelog(player_id, force_fresh=True)  # Force fresh data for testing

if __name__ == "__main__":
    main()