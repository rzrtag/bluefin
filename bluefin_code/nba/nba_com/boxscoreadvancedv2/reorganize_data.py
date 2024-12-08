#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "boxscoreadvancedv2"
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

def get_game_date(game_id: str, df: pd.DataFrame) -> str:
    """
    Try to get game date from the data.
    Format: YYYY-MM-DD
    """
    try:
        # First try to get GAME_DATE_EST from the data
        if 'GAME_DATE_EST' in df.columns:
            date_str = df['GAME_DATE_EST'].iloc[0]
            return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        pass
    
    # If we can't get date from data, try to infer from game ID
    # Game IDs starting with 0022 are regular season games
    if game_id.startswith('00224'):  # 2024-25 season
        game_num = int(game_id[-4:])  # Last 4 digits
        # Rough estimate: season starts in October
        if game_num <= 200:  # October/November games
            return f"2024-{10 + (game_num // 100):02d}-01"
        elif game_num <= 400:  # December games
            return "2024-12-01"
        else:  # January onwards
            return f"2025-{1 + (game_num - 400) // 100:02d}-01"
    
    # If all else fails, use current date
    print(f"Warning: Could not get date for game {game_id}, using current date")
    return datetime.now().strftime('%Y-%m-%d')

def reorganize_raw_data():
    """Reorganize raw data into YYYY-MM folders."""
    print("\nReorganizing raw data...")
    
    # First, handle files in season folders
    season_dir = RAW_DIR / "2024-25"
    if season_dir.exists():
        for file_path in season_dir.glob("*.csv"):
            try:
                # Read the data to get the date
                df = pd.read_csv(file_path)
                game_id = file_path.stem  # filename without extension
                game_date = get_game_date(game_id, df)
                year_month = game_date[:7]  # YYYY-MM
                
                # Create new directory
                new_dir = RAW_DIR / year_month
                new_dir.mkdir(parents=True, exist_ok=True)
                
                # Move file to new location
                new_path = new_dir / file_path.name
                print(f"Moving {file_path.name} to {new_path}")
                shutil.move(str(file_path), str(new_path))
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        # Try to remove season directory if empty
        try:
            season_dir.rmdir()
            print(f"Removed empty directory {season_dir}")
        except:
            pass
    
    # Then handle any remaining files in raw directory
    for file_path in RAW_DIR.glob("*.csv"):
        try:
            # Skip if already in a YYYY-MM folder
            if len(file_path.parts) >= 2 and file_path.parts[-2].replace('-', '').isdigit():
                continue
                
            # Read the data to get the date
            df = pd.read_csv(file_path)
            game_id = file_path.stem  # filename without extension
            game_date = get_game_date(game_id, df)
            year_month = game_date[:7]  # YYYY-MM
            
            # Create new directory
            new_dir = RAW_DIR / year_month
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file to new location
            new_path = new_dir / file_path.name
            print(f"Moving {file_path.name} to {new_path}")
            shutil.move(str(file_path), str(new_path))
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

def reorganize_processed_data():
    """Reorganize processed data into YYYY-MM folders."""
    print("\nReorganizing processed data...")
    
    # First, handle files in season folders
    season_dir = PROCESSED_DIR / "2024-25"
    if season_dir.exists():
        for file_path in season_dir.glob("*.csv"):
            try:
                # Read the data to get the date
                df = pd.read_csv(file_path)
                game_id = file_path.stem.replace('advanced_', '')  # remove prefix
                game_date = get_game_date(game_id, df)
                year_month = game_date[:7]  # YYYY-MM
                
                # Create new directory
                new_dir = PROCESSED_DIR / year_month
                new_dir.mkdir(parents=True, exist_ok=True)
                
                # Move file to new location
                new_path = new_dir / file_path.name
                print(f"Moving {file_path.name} to {new_path}")
                shutil.move(str(file_path), str(new_path))
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        # Try to remove season directory if empty
        try:
            season_dir.rmdir()
            print(f"Removed empty directory {season_dir}")
        except:
            pass
    
    # Then handle any remaining files
    for file_path in PROCESSED_DIR.glob("*.csv"):
        try:
            # Skip if already in a YYYY-MM folder
            if len(file_path.parts) >= 2 and file_path.parts[-2].replace('-', '').isdigit():
                continue
                
            # Read the data to get the date
            df = pd.read_csv(file_path)
            game_id = file_path.stem.replace('advanced_', '')  # remove prefix
            game_date = get_game_date(game_id, df)
            year_month = game_date[:7]  # YYYY-MM
            
            # Create new directory
            new_dir = PROCESSED_DIR / year_month
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file to new location
            new_path = new_dir / file_path.name
            print(f"Moving {file_path.name} to {new_path}")
            shutil.move(str(file_path), str(new_path))
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

def main():
    """Main entry point."""
    print("NBA Advanced Stats Data Reorganizer")
    print("----------------------------------")
    
    # Create directories if they don't exist
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Reorganize data
    reorganize_raw_data()
    reorganize_processed_data()
    
    print("\nReorganization complete!")

if __name__ == "__main__":
    main() 