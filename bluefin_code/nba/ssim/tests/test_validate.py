#!/usr/bin/env python3

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import yaml

from bluefin_code.nba.ssim.validate import (
    validate_raw_data,
    validate_game_data,
    validate_player_data,
    validate_output_format
)

@pytest.fixture
def sample_raw_data() -> pd.DataFrame:
    """Create sample raw data for testing."""
    return pd.DataFrame({
        'name': ['Player 1', 'Player 2'],
        'team': ['LAL', 'BOS'],
        'opponent': ['BOS', 'LAL'],
        'status': ['ACTIVE', 'ACTIVE'],
        'points': [20.5, 25.3],
        'minutes': [32.1, 34.5],
        'rebounds': [5.2, 6.7],
        'assists': [4.1, 3.8],
        'steals': [1.1, 0.9],
        'blocks': [0.5, 0.7],
        'turnovers': [2.1, 1.8],
        'three_pt_fg': [2.3, 3.1],
        'timestamp': [datetime.now().timestamp()] * 2,
        'version': ['2.0'] * 2
    })

@pytest.fixture
def sample_processed_data() -> pd.DataFrame:
    """Create sample processed data for testing."""
    return pd.DataFrame({
        'name': ['Player 1', 'Player 2'],
        'team': ['LAL', 'BOS'],
        'opponent': ['BOS', 'LAL'],
        'status': ['ACTIVE', 'ACTIVE'],
        'points': [20.5, 25.3],
        'minutes': [32.1, 34.5],
        'rebounds': [5.2, 6.7],
        'assists': [4.1, 3.8],
        'steals': [1.1, 0.9],
        'blocks': [0.5, 0.7],
        'turnovers': [2.1, 1.8],
        'three_pt_fg': [2.3, 3.1],
        'pra': [29.8, 35.8],
        'pr': [25.7, 32.0],
        'pa': [24.6, 29.1],
        'ra': [9.3, 10.5],
        'stocks': [1.6, 1.6],
        'timestamp': [datetime.now().timestamp()] * 2,
        'version': ['2.0'] * 2
    })

@pytest.fixture
def config() -> dict:
    """Load test configuration."""
    with open(Path(__file__).parent.parent / "config/config.yaml") as f:
        return yaml.safe_load(f)

def test_validate_raw_data(sample_raw_data):
    """Test raw data validation."""
    # Valid data should pass
    assert validate_raw_data(sample_raw_data) is True
    
    # Test missing columns
    bad_data = sample_raw_data.drop('points', axis=1)
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_raw_data(bad_data)
    
    # Test invalid status
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'status'] = 'INVALID'
    with pytest.raises(ValueError, match="Invalid status values"):
        validate_raw_data(bad_data)

def test_validate_game_data(sample_raw_data):
    """Test game data validation."""
    # Add game fields
    sample_raw_data['home_team'] = ['LAL', 'BOS']
    sample_raw_data['away_team'] = ['BOS', 'LAL']
    sample_raw_data['game_time'] = datetime.now()
    
    # Valid data should pass
    assert validate_game_data(sample_raw_data) is True
    
    # Test duplicate games
    bad_data = pd.concat([sample_raw_data, sample_raw_data])
    with pytest.warns(UserWarning, match="duplicate games"):
        validate_game_data(bad_data)

def test_validate_player_data(sample_raw_data):
    """Test player data validation."""
    # Valid data should pass
    assert validate_player_data(sample_raw_data) is True
    
    # Test unreasonable stats
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'assists'] = bad_data.loc[0, 'points'] + 1
    with pytest.warns(UserWarning, match="more assists than points"):
        validate_player_data(bad_data)

def test_validate_output_format(sample_processed_data, config):
    """Test output format validation."""
    # Valid data should pass
    assert validate_output_format(sample_processed_data) is True
    
    # Test missing core fields
    bad_data = sample_processed_data.drop('points', axis=1)
    with pytest.raises(ValueError, match="Missing core field"):
        validate_output_format(bad_data)
    
    # Test missing calculated fields
    bad_data = sample_processed_data.drop('pra', axis=1)
    with pytest.raises(ValueError, match="Missing calculated field"):
        validate_output_format(bad_data) 