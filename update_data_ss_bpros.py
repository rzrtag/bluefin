#!/usr/bin/env python3

import argparse
import logging
from datetime import datetime
from pathlib import Path

from bluefin_code.nba.bettingpros.run_bpro_pipeline import run_pipeline as run_bpro_pipeline
from bluefin_code.nba.ssim.fetch import fetch_projections
from bluefin_code.nba.ssim.process import process_data

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format')
    parser.add_argument('--force', action='store_true', help='Force update even if no changes')
    args = parser.parse_args()

    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()

    date_str = date.strftime('%Y-%m-%d')

    try:
        # Run BettingPros pipeline
        logger.info("\n=== Running BettingPros Pipeline ===")
        run_bpro_pipeline(date, args.force)

        # Run SaberSim pipeline
        logger.info("\n=== Running SaberSim Pipeline ===")
        # First fetch new projections
        data = fetch_projections()
        if data:
            logger.info("✓ Projections updated")
            # Then process the data - note that process_data only takes the data argument
            process_data(data)
            logger.info("✓ Processing complete")
        else:
            logger.error("Failed to fetch projections")

    except Exception as e:
        logger.error(f"Error during update: {str(e)}")
        raise

if __name__ == '__main__':
    main() 