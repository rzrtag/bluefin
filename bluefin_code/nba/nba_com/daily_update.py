#!/usr/bin/env python3

from datetime import datetime, timedelta
import time
from pathlib import Path
from typing import List, Optional

from get_game_ids import get_game_ids
from gamerotation.collector import save_rotation_stats
from playergamelog.collector import save_player_gamelog
from boxscoreadvancedv2.collector import get_player_ids_from_game

def check_game_exists(game_id: str, date: str) -> bool:
    """Check if game data already exists in both gamerotation and boxscore."""
    # Get year-month for gamerotation
    year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
    
    # Check gamerotation file
    rotation_path = Path("bluefin_data/nba/nba_com/gamerotation/processed") / year_month / f"rotation_{game_id}.csv"
    
    return rotation_path.exists()

def collect_daily_data(date: Optional[str] = None, force_fresh: bool = False) -> None:
    """Collect both game rotation and player game log data for a specific date."""
    # Use yesterday if no date provided
    if date is None:
        yesterday = datetime.now() - timedelta(days=1)
        date = yesterday.strftime("%Y-%m-%d")
    
    print(f"\nCollecting NBA data for {date}")
    print("=" * 40)
    
    # 1. Get game IDs for the date
    game_ids_df = get_game_ids(force_fresh=force_fresh)
    if game_ids_df is None:
        print("Failed to get game IDs")
        return
    
    # Filter for the given date
    games = game_ids_df[game_ids_df['game_date'] == date]
    if len(games) == 0:
        print(f"No games found for {date}")
        return
    
    print(f"\nFound {len(games)} games on {date}:")
    for _, game in games.iterrows():
        print(f"- {game['matchup']} (ID: {game['game_id']})")
    
    # 2. Process each game
    for _, game in games.iterrows():
        game_id = game['game_id']
        
        # Skip if game already processed (unless force_fresh)
        if not force_fresh and check_game_exists(game_id, date):
            print(f"\nSkipping already processed game: {game['matchup']} ({game_id})")
            continue
            
        print(f"\nProcessing game: {game['matchup']} ({game_id})")
        
        # 2a. Get game rotation data
        print("\nCollecting game rotation data...")
        save_rotation_stats(game_id, date, force_fresh)
        time.sleep(0.25)  # Quarter second pause between API calls
        
        # 2b. Get player game logs
        print("\nCollecting player game logs...")
        # Get player IDs from the game
        player_ids = get_player_ids_from_game(game_id, date)
        if player_ids:
            print(f"Found {len(player_ids)} players")
            for player_id in player_ids:
                save_player_gamelog(player_id, force_fresh=force_fresh)
                time.sleep(0.05)  # 50ms between player requests
        
        print(f"\nCompleted processing game {game_id}")
        time.sleep(0.25)  # Quarter second pause between games

def main():
    """Main entry point with basic argument handling."""
    import sys
    
    print("\nNBA Daily Data Collector")
    print("======================")
    
    # Handle optional date argument
    date = None
    force_fresh = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--force":
            force_fresh = True
        else:
            date = sys.argv[1]
            if len(sys.argv) > 2 and sys.argv[2] == "--force":
                force_fresh = True
    
    collect_daily_data(date, force_fresh)

if __name__ == "__main__":
    main() 