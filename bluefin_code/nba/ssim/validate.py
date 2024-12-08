#!/usr/bin/env python3

"""Validation functions for SaberSim data."""

import pandas as pd
import numpy as np
from typing import Union, List, Dict
import logging
from pathlib import Path
import yaml

# Load config
CONFIG_PATH = Path(__file__).parent / "config/config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

def validate_raw_data(df: pd.DataFrame) -> bool:
    """Validate raw data structure and basic content."""
    required_fields = CONFIG['required_fields']
    required_player_fields = CONFIG['required_player_fields']
    
    # Check required fields
    missing_fields = [f for f in required_fields if f not in df.columns]
    if missing_fields:
        raise ValueError(f"Missing required columns: {missing_fields}")
    
    # Check player fields
    missing_player_fields = [f for f in required_player_fields if f not in df.columns]
    if missing_player_fields:
        raise ValueError(f"Missing required player fields: {missing_player_fields}")
    
    # Validate status values
    valid_statuses = ['ACTIVE', 'OUT', 'GTD', 'QUESTIONABLE', 'PROBABLE']
    invalid_status = ~df['status'].isin(valid_statuses)
    if invalid_status.any():
        raise ValueError(f"Invalid status values: {df.loc[invalid_status, 'status'].unique()}")
    
    return True

def validate_game_data(df: pd.DataFrame) -> bool:
    """Validate game-level data."""
    # Check for duplicate games
    game_cols = ['home_team', 'away_team', 'game_time']
    dupes = df[game_cols].duplicated()
    if dupes.any():
        logging.warning(f"Found {dupes.sum()} duplicate games")
    
    # Validate game times
    if pd.to_datetime(df['game_time']).isnull().any():
        raise ValueError("Invalid game times found")
    
    # Check team codes
    valid_teams = set(CONFIG['team_codes'].values())
    invalid_home = ~df['home_team'].isin(valid_teams)
    invalid_away = ~df['away_team'].isin(valid_teams)
    
    if invalid_home.any() or invalid_away.any():
        raise ValueError("Invalid team codes found")
    
    return True

def validate_player_data(df: pd.DataFrame) -> bool:
    """Validate player-level statistics."""
    # Check for impossible stats
    if (df['assists'] > df['points']).any():
        logging.warning("Found players with more assists than points")
    
    if (df['blocks'] > df['points']).any():
        logging.warning("Found players with more blocks than points")
    
    # Validate percentages
    pct_cols = ['fg_pct', 'three_pt_pct', 'ft_pct']
    for col in pct_cols:
        if col in df.columns:
            invalid_pct = (df[col] < 0) | (df[col] > 1)
            if invalid_pct.any():
                raise ValueError(f"Invalid {col} values found")
    
    # Check for unreasonable projections
    if (df['points'] > 100).any():
        logging.warning("Found unusually high point projections")
    
    if (df['rebounds'] > 40).any():
        logging.warning("Found unusually high rebound projections")
    
    if (df['assists'] > 30).any():
        logging.warning("Found unusually high assist projections")
    
    return True

def validate_output_format(df: pd.DataFrame) -> bool:
    """Validate the final output format."""
    # Load column definitions
    with open(Path(__file__).parent / "config/columns.yaml") as f:
        COLUMNS = yaml.safe_load(f)
    
    # Check core fields
    for field, dtype in COLUMNS['core'].items():
        if field not in df.columns:
            raise ValueError(f"Missing core field: {field}")
        if not pd.api.types.is_dtype_equal(df[field].dtype, dtype):
            raise ValueError(f"Invalid dtype for {field}: expected {dtype}, got {df[field].dtype}")
    
    # Check calculated fields
    for field in COLUMNS['props']:
        if field not in df.columns:
            raise ValueError(f"Missing calculated field: {field}")
    
    # Validate percentiles
    for field in COLUMNS['percentiles']:
        if field not in df.columns:
            raise ValueError(f"Missing percentile field: {field}")
        
        # Check percentile ordering
        base = field.split('_')[0]
        p25 = f"{base}_25"
        p50 = f"{base}_50"
        p75 = f"{base}_75"
        
        if not (df[p25] <= df[p50]).all() or not (df[p50] <= df[p75]).all():
            raise ValueError(f"Invalid percentile ordering for {base}")
    
    return True 