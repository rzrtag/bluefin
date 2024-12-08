#!/usr/bin/env python3

from pathlib import Path
import shutil

# Get the current directory
current_dir = Path(__file__).parent
extra_dir = current_dir / "nba_com"

if extra_dir.exists():
    print(f"\nMoving contents from {extra_dir} to {current_dir}")
    
    # Move all contents up one level
    for item in extra_dir.iterdir():
        target = current_dir / item.name
        print(f"Moving {item.name}")
        shutil.move(str(item), str(target))
    
    # Remove the empty directory
    print(f"Removing empty directory {extra_dir}")
    extra_dir.rmdir()
    
    print("\nDirectory structure fixed!")
else:
    print("\nNo extra nba_com directory found. Structure looks correct.") 