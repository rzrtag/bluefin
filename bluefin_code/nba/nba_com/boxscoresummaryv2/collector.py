#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from nba_api.stats.endpoints import boxscoresummaryv2

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "boxscoresummaryv2"
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

def get_summary_stats(game_id: str, date: str, force_fresh: bool = False) -> Optional[Dict[str, pd.DataFrame]]:
    """Get summary stats for a game from NBA.com."""
    # Ensure game_id is a string and properly formatted
    game_id = str(game_id)
    if len(game_id) == 10:  # Already full format (0022300001)
        api_game_id = game_id
    elif len(game_id) == 8:  # Short format (22300001)
        api_game_id = f"00{game_id}"
    else:
        print(f"Invalid game ID format: {game_id}")
        return None
    
    print(f"\nFetching summary stats for game {game_id}")
    
    # Get year-month for organization
    year_month = get_year_month(date)
    
    # Create cache path
    cache_dir = RAW_DIR / year_month
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Cache paths for each result set
    cache_paths = {
        'summary': cache_dir / f"{game_id}_summary.csv",
        'line': cache_dir / f"{game_id}_line.csv"
    }
    
    # Return cached data if it exists and we're not forcing fresh
    if not force_fresh and all(p.exists() for p in cache_paths.values()):
        print(f"Using cached data from {cache_dir}")
        return {
            'summary': pd.read_csv(cache_paths['summary']),
            'line': pd.read_csv(cache_paths['line'])
        }
    
    try:
        print("Fetching data from NBA API...")
        boxscore = boxscoresummaryv2.BoxScoreSummaryV2(game_id=api_game_id)
        
        # Get all result sets
        all_dfs = boxscore.get_data_frames()
        
        if not all_dfs:
            print("No data returned from API")
            return None
            
        # Get relevant result sets
        game_summary = all_dfs[0]  # GameSummary
        line_score = all_dfs[5]    # LineScore
        
        # Cache the raw data
        game_summary.to_csv(cache_paths['summary'], index=False)
        line_score.to_csv(cache_paths['line'], index=False)
        print(f"Cached raw data to {cache_dir}")
        
        return {
            'summary': game_summary,
            'line': line_score
        }
        
    except Exception as e:
        print(f"Error getting data for game {game_id}: {str(e)}")
        return None

def process_summary_stats(data: Optional[Dict[str, pd.DataFrame]]) -> Optional[Dict[str, pd.DataFrame]]:
    """Process raw summary stats into clean format."""
    if data is None:
        return None
        
    game_summary = data['summary']
    line_score = data['line']
    
    # Process game summary
    game_cols = {
        'GAME_ID': 'game_id',
        'GAME_STATUS_ID': 'game_status',
        'GAME_STATUS_TEXT': 'game_status_text',
        'GAMECODE': 'game_code',
        'HOME_TEAM_ID': 'home_team_id',
        'VISITOR_TEAM_ID': 'visitor_team_id',
        'SEASON': 'season',
        'GAME_DATE_EST': 'game_date',
        'LIVE_PERIOD': 'period',
        'LIVE_PC_TIME': 'game_clock',
        'NATL_TV_BROADCASTER_ABBREVIATION': 'broadcaster'
    }
    
    # Only select columns that exist
    available_game_cols = [col for col in game_cols.keys() if col in game_summary.columns]
    game_summary = game_summary[available_game_cols].rename(columns={col: game_cols[col] for col in available_game_cols})
    
    # Process line score
    line_cols = {
        'GAME_ID': 'game_id',
        'TEAM_ID': 'team_id',
        'TEAM_ABBREVIATION': 'team',
        'TEAM_CITY_NAME': 'team_city',
        'TEAM_NICKNAME': 'team_name',
        'TEAM_WINS_LOSSES': 'record',
        'PTS': 'points',
        'PTS_QTR1': 'points_q1',
        'PTS_QTR2': 'points_q2',
        'PTS_QTR3': 'points_q3',
        'PTS_QTR4': 'points_q4',
        'PTS_OT1': 'points_ot1',
        'PTS_OT2': 'points_ot2',
        'PTS_OT3': 'points_ot3',
        'PTS_OT4': 'points_ot4'
    }
    
    # Only select columns that exist
    available_line_cols = [col for col in line_cols.keys() if col in line_score.columns]
    line_score = line_score[available_line_cols].rename(columns={col: line_cols[col] for col in available_line_cols})
    
    # Convert points to numeric
    point_cols = [col for col in line_score.columns if 'points' in col.lower()]
    for col in point_cols:
        line_score[col] = pd.to_numeric(line_score[col], errors='coerce').fillna(0)
    
    # Print some debug info
    print(f"\nProcessed game summary and line score data")
    print(f"Game summary rows: {len(game_summary)}")
    print(f"Line score rows: {len(line_score)}")
    
    return {
        'summary': game_summary,
        'line': line_score
    }

def save_summary_stats(game_id: str, date: str, force_fresh: bool = False) -> None:
    """Get and save summary stats for a game."""
    print(f"\nProcessing game {game_id} from {date}")
    
    # Get raw data
    raw_data = get_summary_stats(game_id, date, force_fresh)
    if raw_data is None:
        print("Failed to get raw data")
        return
    
    # Process data
    data = process_summary_stats(raw_data)
    if data is None:
        print("Failed to process data")
        return
    
    # Get year-month
    year_month = get_year_month(date)
    save_dir = PROCESSED_DIR / year_month
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Save processed data
    game_path = save_dir / f"summary_{game_id}.csv"
    line_path = save_dir / f"line_{game_id}.csv"
    
    data['summary'].to_csv(game_path, index=False)
    data['line'].to_csv(line_path, index=False)
    print(f"Saved processed data to {save_dir}")

def main():
    """Example usage."""
    print("\nNBA Summary Stats Collector")
    print("-------------------------")
    
    # Test with a known game ID
    test_game = ("0022300001", "2023-10-24")  # First game of 2023-24 season
    save_summary_stats(test_game[0], test_game[1], force_fresh=True)

if __name__ == "__main__":
    main() 