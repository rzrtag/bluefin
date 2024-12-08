"""NBA utilities module."""

import json
from pathlib import Path

# Load configurations
CONFIG_DIR = Path(__file__).parent

with open(CONFIG_DIR / "bks_config.json") as f:
    BOOKS_CONFIG = json.load(f)

with open(CONFIG_DIR / "plyr_mrkts.json") as f:
    MARKETS_CONFIG = json.load(f)

def get_market_name(market_id: str) -> str:
    """Get standardized market name from market ID."""
    for market in MARKETS_CONFIG['markets'].values():
        if market['market_id'] == market_id:
            return market['abbreviation']
    return 'unknown'

def get_book_name(book: str) -> str:
    """Get standardized book name."""
    book = book.lower()
    if book in BOOKS_CONFIG['sportsbooks']:
        return BOOKS_CONFIG['sportsbooks'][book]['abbreviation']
    return book 