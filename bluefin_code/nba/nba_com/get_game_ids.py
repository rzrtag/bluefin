#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
from nba_api.stats.endpoints import leaguegamefinder

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com"
CACHE_DIR = BASE_DIR / "game_ids"

# Define seasons and dates
CURRENT_SEASON = "2024-25"  # Current season
LAST_SEASON = "2023-24"    # Last season
ALL_SEASONS = [LAST_SEASON, CURRENT_SEASON]  # Only two seasons

# Regular season dates
SEASON_DATES = {
    "2024-25": {
        "start": "2024-10-22",  # Opening night 2024-25
        "end": "2024-12-07"     # Current date
    },
    "2023-24": {
        "start": "2023-10-24",  # Opening night 2023-24
        "end": "2024-04-14"     # Regular season end
    }
}

def get_game_ids_for_season(season: str = CURRENT_SEASON, force_fresh: bool = False) -> Optional[pd.DataFrame]:
    """Get all game IDs for a season from NBA.com."""
    print(f"\nFetching game IDs for season {season}")
    
    # Create cache path
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"games_{season.replace('-', '_')}.csv"
    
    # Return cached data if it exists and we're not forcing fresh
    if not force_fresh and cache_path.exists():
        print(f"Using cached data from {cache_path}")
        df = pd.read_csv(cache_path)
        
        # Filter for regular season dates
        dates = SEASON_DATES[season]
        mask = (df['game_date'] >= dates['start']) & (df['game_date'] <= dates['end'])
        return df[mask]
    
    try:
        print("Fetching data from NBA API...")
        # Get data from NBA API
        gamefinder = leaguegamefinder.LeagueGameFinder(
            season_nullable=season,
            league_id_nullable="00",  # NBA
            season_type_nullable="Regular Season"
        )
        
        # Convert to DataFrame
        df = gamefinder.get_data_frames()[0]
        print(f"Got data with {len(df)} rows")
        
        # Process the data
        df = process_game_ids(df)
        
        # Add season column
        df['season'] = season
        
        # Filter for regular season dates
        dates = SEASON_DATES[season]
        mask = (df['game_date'] >= dates['start']) & (df['game_date'] <= dates['end'])
        df = df[mask]
        
        # Cache the processed data
        df.to_csv(cache_path, index=False)
        print(f"Cached data to {cache_path}")
        
        return df
        
    except Exception as e:
        print(f"Error getting game IDs: {str(e)}")
        return None

def get_game_ids(seasons: List[str] = ALL_SEASONS, force_fresh: bool = False) -> Optional[pd.DataFrame]:
    """Get game IDs for multiple seasons."""
    all_games = []
    
    for season in seasons:
        df = get_game_ids_for_season(season, force_fresh)
        if df is not None:
            all_games.append(df)
    
    if not all_games:
        return None
    
    # Combine all seasons
    return pd.concat(all_games, ignore_index=True)

def process_game_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Process raw game data into clean format."""
    # Select and rename columns
    cols = {
        'GAME_ID': 'game_id',
        'GAME_DATE': 'game_date',
        'MATCHUP': 'matchup',
        'WL': 'win_loss',
        'TEAM_ID': 'team_id',
        'TEAM_ABBREVIATION': 'team'
    }
    
    df = df[cols.keys()].rename(columns=cols)
    
    # Convert game date to YYYY-MM-DD format
    df['game_date'] = pd.to_datetime(df['game_date']).dt.strftime('%Y-%m-%d')
    
    # Sort by date and game ID
    df = df.sort_values(['game_date', 'game_id'])
    
    # Remove duplicate games (each game appears twice, once for each team)
    df = df.drop_duplicates(subset=['game_id'])
    
    # Print some debug info
    print(f"\nProcessed game IDs:")
    print(f"Total games: {len(df)}")
    print("\nGames by month:")
    print(df['game_date'].str[:7].value_counts().sort_index())
    
    return df

def get_game_ids_by_date(date: str, game_ids_df: Optional[pd.DataFrame] = None) -> List[str]:
    """Get game IDs for a specific date."""
    if game_ids_df is None:
        game_ids_df = get_game_ids()
        if game_ids_df is None:
            return []
    
    # Filter for the given date
    games = game_ids_df[game_ids_df['game_date'] == date]
    return games['game_id'].tolist()

def get_season_for_date(date: str) -> str:
    """Determine which season a date belongs to."""
    dt = datetime.strptime(date, "%Y-%m-%d")
    year = dt.year
    month = dt.month
    
    # If date is between October and December, it's the next year's season
    if month >= 10:
        return f"{year}-{str(year+1)[2:]}"
    # If date is between January and June, it's the current year's season
    else:
        return f"{year-1}-{str(year)[2:]}"

def main():
    """Example usage."""
    print("\nNBA Game ID Collector")
    print("-------------------")
    
    # Get all game IDs for both seasons
    df = get_game_ids(force_fresh=True)
    if df is None:
        print("Failed to get game IDs")
        return
    
    # Example: Get games for specific dates across seasons
    test_dates = [
        SEASON_DATES[LAST_SEASON]['start'],    # Last season opening night
        SEASON_DATES[LAST_SEASON]['end'],      # Last season end
        SEASON_DATES[CURRENT_SEASON]['start'], # Current season opening night
        SEASON_DATES[CURRENT_SEASON]['end']    # Current date
    ]
    
    for date in test_dates:
        game_ids = get_game_ids_by_date(date, df)
        season = get_season_for_date(date)
        print(f"\nGames on {date} (Season {season}):")
        for game_id in game_ids:
            game = df[df['game_id'] == game_id].iloc[0]
            print(f"- {game['matchup']} (ID: {game_id})")

if __name__ == "__main__":
    main() 