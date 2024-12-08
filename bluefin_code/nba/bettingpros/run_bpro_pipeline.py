#!/usr/bin/env python3

import os
import argparse
import sys
from datetime import datetime, timedelta
import logging
from pathlib import Path

# Add project root to Python path
file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(file_dir, "../../../"))
sys.path.append(project_root)

from bluefin_code.nba.bettingpros.fetch import (
    fetch_sportsbook_data, create_default_config,
    get_data_dir
)
from bluefin_code.nba.bettingpros.process import process_date

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def get_date_range(start_date: str, end_date: str | None = None) -> list[str]:
    """Get list of dates between start and end (inclusive)."""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()
    
    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    return dates

def run_pipeline(date: datetime, force: bool = False) -> None:
    """
    Run the full pipeline for processing betting data
    
    Args:
        date: Date to process
        force: Whether to force update even if no changes
    """
    date_str = date.strftime('%Y-%m-%d')
    logger.info(f"\n=== BPRO {date_str} ===")
    
    try:
        # Create config
        config = create_default_config()
        
        # Fetch props for each sportsbook
        results = []
        for book in config.sportsbooks:
            output_file, stats = fetch_sportsbook_data(book, date_str, config, force=force)
            if output_file:
                results.append((book.abbreviation, stats))
        
        # Process raw files into standardized format
        process_date(date_str)
        
        logger.info("✓ Done")
        
    except Exception as e:
        logger.error(f"Pipeline error for {date_str}: {str(e)}")
        raise

def main():
    """Main pipeline function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='Single date to process (YYYY-MM-DD)')
    parser.add_argument('--start-date', help='Start date for range (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date for range (YYYY-MM-DD)')
    parser.add_argument('--force', action='store_true', help='Force fetch new data')
    args = parser.parse_args()
    
    # Get dates to process
    if args.date:
        dates = [args.date]
    elif args.start_date:
        dates = get_date_range(args.start_date, args.end_date)
    else:
        dates = [datetime.now().strftime('%Y-%m-%d')]
    
    # Process each date
    for date in dates:
        logger.info(f"\n=== BPRO {date} ===")
        
        try:
            # Run pipeline
            run_pipeline(date, args.force)
            
        except Exception as e:
            logger.error(f"Pipeline error for {date}: {str(e)}")
            continue

if __name__ == "__main__":
    main()  