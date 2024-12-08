#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
NBA_COM_DIR = DATA_ROOT / "nba" / "nba_com"

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

def reorganize_directory(data_dir: Path):
    """Reorganize data files in a directory into YYYY-MM folders."""
    print(f"\nReorganizing {data_dir}...")
    
    raw_dir = data_dir / "raw"
    processed_dir = data_dir / "processed"
    
    # Create directories if they don't exist
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # First handle season folders in raw directory
    for season_dir in raw_dir.glob("20*-*"):
        if season_dir.is_dir():
            print(f"\nProcessing season directory: {season_dir}")
            for file_path in season_dir.glob("*.csv"):
                try:
                    # Read the data to get the date
                    df = pd.read_csv(file_path)
                    game_id = file_path.stem  # filename without extension
                    game_date = get_game_date(game_id, df)
                    year_month = game_date[:7]  # YYYY-MM
                    
                    # Create new directory
                    new_dir = raw_dir / year_month
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
    
    # Handle any remaining files in raw directory
    for file_path in raw_dir.glob("*.csv"):
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
            new_dir = raw_dir / year_month
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file to new location
            new_path = new_dir / file_path.name
            print(f"Moving {file_path.name} to {new_path}")
            shutil.move(str(file_path), str(new_path))
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    # Handle season folders in processed directory
    for season_dir in processed_dir.glob("20*-*"):
        if season_dir.is_dir():
            print(f"\nProcessing season directory: {season_dir}")
            for file_path in season_dir.glob("*.csv"):
                try:
                    # Read the data to get the date
                    df = pd.read_csv(file_path)
                    game_id = file_path.stem.split('_')[-1]  # Get game ID from filename
                    game_date = get_game_date(game_id, df)
                    year_month = game_date[:7]  # YYYY-MM
                    
                    # Create new directory
                    new_dir = processed_dir / year_month
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
    
    # Handle any remaining files in processed directory
    for file_path in processed_dir.glob("*.csv"):
        try:
            # Skip if already in a YYYY-MM folder
            if len(file_path.parts) >= 2 and file_path.parts[-2].replace('-', '').isdigit():
                continue
                
            # Read the data to get the date
            df = pd.read_csv(file_path)
            game_id = file_path.stem.split('_')[-1]  # Get game ID from filename
            game_date = get_game_date(game_id, df)
            year_month = game_date[:7]  # YYYY-MM
            
            # Create new directory
            new_dir = processed_dir / year_month
            new_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file to new location
            new_path = new_dir / file_path.name
            print(f"Moving {file_path.name} to {new_path}")
            shutil.move(str(file_path), str(new_path))
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

def main():
    """Main entry point."""
    print("NBA.com Data Reorganizer")
    print("----------------------")
    
    # Get all NBA.com data directories
    nba_com_dirs = [d for d in NBA_COM_DIR.iterdir() if d.is_dir()]
    
    for data_dir in nba_com_dirs:
        reorganize_directory(data_dir)
    
    print("\nReorganization complete!")

if __name__ == "__main__":
    main() 