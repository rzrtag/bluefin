#!/usr/bin/env python3

from pathlib import Path
from ....endpoints.core.base_collector import BaseCollector
from .collector import BoxscoreSummaryCollector

class BoxscoreSummarySeasonCollector(BaseCollector):
    """Season collector for NBA.com boxscoresummaryv2 endpoint."""
    
    def __init__(self):
        """Initialize the collector."""
        super().__init__('nba_com/boxscoresummaryv2')
        self.collector = BoxscoreSummaryCollector()
    
    def save_stats(self, game_id: str, force_fresh: bool = False):
        """Save stats for a game."""
        self.collector.save_stats(game_id, force_fresh)

def main():
    """Main entry point."""
    collector = BoxscoreSummarySeasonCollector()
    collector.run()

if __name__ == "__main__":
    main() 