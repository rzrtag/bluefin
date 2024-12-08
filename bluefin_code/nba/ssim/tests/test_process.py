#!/usr/bin/env python3

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import yaml

from bluefin_code.nba.ssim.process import (
    calculate_aggregated_props,
    calculate_percentiles,
    process_raw_data,
    calculate_advanced_metrics
)

from bluefin_code.nba.ssim.validate import (
    validate_raw_data,
    validate_game_data,
    validate_player_data
)

@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Create sample data for testing."""
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
def config() -> dict:
    """Load test configuration."""
    with open(Path(__file__).parent.parent / "config/config.yaml") as f:
        return yaml.safe_load(f)

def test_validate_raw_data(sample_data):
    """Test data validation."""
    # Valid data should pass
    assert validate_raw_data(sample_data) is True
    
    # Test missing columns
    bad_data = sample_data.drop('points', axis=1)
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_raw_data(bad_data)
    
    # Test invalid status
    bad_data = sample_data.copy()
    bad_data.loc[0, 'status'] = 'INVALID'
    with pytest.raises(ValueError, match="Invalid status values"):
        validate_raw_data(bad_data)

def test_calculate_aggregated_props(sample_data):
    """Test aggregated prop generation."""
    result = calculate_aggregated_props(sample_data)
    
    # Check calculated fields exist
    assert 'pra' in result.columns
    assert 'pr' in result.columns
    assert 'pa' in result.columns
    assert 'ra' in result.columns
    assert 'stocks' in result.columns
    
    # Check calculations are correct
    assert result.loc[0, 'pra'] == 29.8  # 20.5 + 5.2 + 4.1
    assert result.loc[0, 'pr'] == 25.7   # 20.5 + 5.2
    assert result.loc[0, 'pa'] == 24.6   # 20.5 + 4.1
    assert result.loc[0, 'ra'] == 9.3    # 5.2 + 4.1
    assert result.loc[0, 'stocks'] == 1.6 # 1.1 + 0.5

def test_calculate_percentiles(sample_data):
    """Test percentile calculations."""
    stats = ['points', 'rebounds', 'assists']
    result = calculate_percentiles(sample_data, stats)
    
    # Check percentile columns exist
    for stat in stats:
        assert f'{stat}_25' in result.columns
        assert f'{stat}_50' in result.columns
        assert f'{stat}_75' in result.columns
    
    # Check percentile values make sense
    assert result['points_25'].iloc[0] <= result['points_50'].iloc[0]
    assert result['points_50'].iloc[0] <= result['points_75'].iloc[0]

def test_full_processing(sample_data, config, tmp_path):
    """Test end-to-end processing."""
    # Setup test environment
    test_date = "2024-12-04"
    test_dir = tmp_path / "nba/ssim/raw/2024-12"
    test_dir.mkdir(parents=True)
    
    # Save test data
    sample_data.to_json(test_dir / f"NBA_{test_date}_raw.json", orient='records')
    
    # Run processing
    result = process_raw_data(sample_data, config)
    
    # Check output format
    assert 'name' in result.columns
    assert 'points' in result.columns
    assert 'timestamp' in result.columns
    
    # Check data transformations
    assert len(result) == len(sample_data)
    assert all(result['status'] == 'ACTIVE')

def test_validate_game_data(sample_data):
    """Test game data validation."""
    # Add game fields
    sample_data['home_team'] = ['LAL', 'BOS']
    sample_data['away_team'] = ['BOS', 'LAL']
    sample_data['game_time'] = datetime.now()
    
    # Valid data should pass
    assert validate_game_data(sample_data) is True
    
    # Test duplicate games
    bad_data = pd.concat([sample_data, sample_data])
    with pytest.warns(UserWarning, match="duplicate games"):
        validate_game_data(bad_data)

def test_validate_player_data(sample_data):
    """Test player data validation."""
    # Valid data should pass
    assert validate_player_data(sample_data) is True
    
    # Test unreasonable stats
    bad_data = sample_data.copy()
    bad_data.loc[0, 'assists'] = bad_data.loc[0, 'points'] + 1
    with pytest.warns(UserWarning, match="more assists than points"):
        validate_player_data(bad_data)

def test_process_raw_data(sample_data, config):
    """Test raw data processing."""
    # Process the data
    result = process_raw_data(sample_data, config)
    
    # Check core fields
    assert 'points' in result.columns
    assert 'rebounds' in result.columns
    assert 'assists' in result.columns
    
    # Verify shooting splits
    assert 'fg_pct' in result.columns
    assert 'three_pt_pct' in result.columns
    assert 'ft_pct' in result.columns
    
    # Check rebound breakdowns
    assert 'off_reb_proj' in result.columns
    assert 'def_reb_proj' in result.columns
    assert result['rebounds'].equals(result['off_reb_proj'] + result['def_reb_proj'])
    
    # Validate calculated values
    assert all(result['points'] >= 0)
    assert all(result['fg_pct'] <= 1.0)
    assert all(result['three_pt_pct'] <= 1.0)