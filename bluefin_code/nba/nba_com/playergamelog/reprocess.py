#!/usr/bin/env python3

from pathlib import Path
from collector import process_gamelog
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"
BASE_DIR = DATA_ROOT / "nba" / "nba_com" / "playergamelog"
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

def reprocess_season(season: str):
    """Reprocess all raw files for a given season."""
    print(f"\nReprocessing all gamelog files for {season}...")
    
    # Get all raw files for the season
    raw_files = list(RAW_DIR.glob(f"{season}/*_{season}.csv"))
    total_files = len(raw_files)
    
    print(f"Found {total_files} raw files to reprocess")
    
    # Process each file
    for i, raw_file in enumerate(raw_files, 1):
        player_id = raw_file.stem.split("_")[0]
        print(f"\nProcessing {i}/{total_files}: Player {player_id}")
        
        try:
            # Read raw data
            df = pd.read_csv(raw_file)
            
            # Process data
            processed_df = process_gamelog(df)
            if processed_df is None:
                print(f"Failed to process {raw_file}")
                continue
                
            # Save processed data
            save_dir = PROCESSED_DIR / season
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / f"gamelog_{raw_file.name}"
            processed_df.to_csv(save_path, index=False)
            print(f"Saved processed data to {save_path}")
            
        except Exception as e:
            print(f"Error processing {raw_file}: {str(e)}")
            continue
            
    print(f"\nReprocessing complete for {season}!")

if __name__ == "__main__":
    # Reprocess both seasons
    reprocess_season("2023-24")
    reprocess_season("2024-25") 