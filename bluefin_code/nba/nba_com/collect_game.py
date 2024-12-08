#!/usr/bin/env python3

from pathlib import Path
import sys
from datetime import datetime, timedelta
import time
from typing import Optional, List, Tuple

from boxscoreadvancedv2.collector import save_advanced_stats, get_player_ids_from_game
from playergamelog.collector import save_player_gamelog
from get_game_ids import get_game_ids

def collect_game_data(game_id: str, date: str, season: str = "2024-25", force_fresh: bool = False) -> None:
    """Collect all data for a single game."""
    print(f"\nCollecting data for game {game_id} on {date}")
    
    # Determine season from date
    game_date = datetime.strptime(date, "%Y-%m-%d")
    if game_date < datetime(2024, 7, 1):  # Use July 1 as season boundary
        season = "2023-24"
    else:
        season = "2024-25"
    
    # 1. Get advanced stats (this will cache the raw data)
    save_advanced_stats(game_id, date, force_fresh)
    
    # 2. Get player IDs from the game
    player_ids = get_player_ids_from_game(game_id, date)
    
    # 3. Get game logs for each player
    for player_id in player_ids:
        save_player_gamelog(player_id, season, force_fresh)
        time.sleep(0.05)  # 50ms between player requests

def collect_games(start_date: Optional[str] = None, 
                 end_date: Optional[str] = None,
                 days_back: int = 3,
                 force_fresh: bool = False) -> None:
    """Collect data for multiple games."""
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=days_back)
        start_date = start.strftime("%Y-%m-%d")
    
    # Get game IDs for date range
    game_ids = get_game_ids(["2024-25"], force_fresh=force_fresh)  # Only 2024-25 season
    
    if game_ids is None or len(game_ids) == 0:
        print(f"No games found between {start_date} and {end_date}")
        return
    
    # Filter for date range
    mask = (game_ids['game_date'] >= start_date) & (game_ids['game_date'] <= end_date)
    date_range_df = game_ids[mask]
    
    if len(date_range_df) == 0:
        print(f"No games found between {start_date} and {end_date}")
        return
    
    print(f"\nFound {len(date_range_df)} games to process")
    print(f"Date range: {start_date} to {end_date}")
    
    # Process each game
    for _, row in date_range_df.iterrows():
        collect_game_data(row['game_id'], row['game_date'], force_fresh=force_fresh)
        time.sleep(0.05)  # 50ms between games

def main():
    """Main entry point with command line argument handling."""
    print("\nNBA.com Data Collector")
    print("--------------------")
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "catchup":
            # Catchup mode - look back 30 days
            collect_games(days_back=30)
        elif mode == "full":
            # Full collection mode - 2024-25 season
            collect_games(start_date="2024-10-24", end_date="2024-12-31")  # 2024-25 season only
        else:
            print(f"Unknown mode: {mode}")
            print("Valid modes: catchup, full")
            sys.exit(1)
    else:
        # Default mode - 3 day lookback
        collect_games()

if __name__ == "__main__":
    main() 