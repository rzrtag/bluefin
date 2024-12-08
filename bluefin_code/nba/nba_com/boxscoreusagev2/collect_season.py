#!/usr/bin/env python3

from pathlib import Path
from ....endpoints.core.base_collector import BaseCollector
from .collector import BoxscoreUsageCollector

class BoxscoreUsageSeasonCollector(BaseCollector):
    """Season collector for NBA.com boxscoreusagev2 endpoint."""
    
    def __init__(self):
        """Initialize the collector."""
        super().__init__('nba_com/boxscoreusagev2')
        self.collector = BoxscoreUsageCollector()
    
    def save_stats(self, game_id: str, force_fresh: bool = False):
        """Save stats for a game."""
        self.collector.save_stats(game_id, force_fresh)

def main():
    """Main entry point."""
    collector = BoxscoreUsageSeasonCollector()
    collector.run()

if __name__ == "__main__":
    main() 