#!/usr/bin/env python3

from pathlib import Path
from .collector import PlayerGameLogCollector

def collect_season(force_fresh=False):
    """Collect playergamelog data for the current season."""
    collector = PlayerGameLogCollector()
    collector.collect_season(force_fresh=force_fresh) 