#!/usr/bin/env python3

from pathlib import Path
from .collector import GameRotationCollector

def collect_season(force_fresh=False):
    """Collect gamerotation data for the current season."""
    collector = GameRotationCollector()
    collector.collect_season(force_fresh=force_fresh) 