"""Test validation functions for BettingPros data."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from ..validate import (
    validate_raw_data,
    validate_game_data,
    validate_player_data,
    validate_output,
    MARKET_TYPES,
    SPORTSBOOKS
)

@pytest.fixture
def sample_raw_data() -> pd.DataFrame:
    """Create sample raw data for testing."""
    data = []
    
    # Create props for two players
    players = [
        ('Player 1', 'LAL', 'BOS'),
        ('Player 2', 'BOS', 'LAL')
    ]
    
    for player_name, team, opp in players:
        # Add props for each market type
        for market_id, market_name in MARKET_TYPES.items():
            # Add lines from each sportsbook
            for book_id in SPORTSBOOKS:
                data.append({
                    'player_name': player_name,
                    'team': team,
                    'opponent': opp,
                    'market_type': market_id,
                    'sportsbook_id': book_id,
                    'over_line': 20.5,  # Will be adjusted below
                    'under_line': 20.5,
                    'over_odds': -110,
                    'under_odds': -110
                })
    
    df = pd.DataFrame(data)
    
    # Adjust lines based on market type
    line_adjustments = {
        'points': 20.5,
        'rebounds': 6.5,
        'assists': 4.5,
        'three_pointers_made': 2.5,
        'steals': 1.5,
        'blocks': 1.5,
        'turnovers': 2.5,
        'points_rebounds': 27.5,
        'points_assists': 25.5,
        'rebounds_assists': 11.5,
        'points_rebounds_assists': 32.5
    }
    
    for market_id, market_name in MARKET_TYPES.items():
        if market_name in line_adjustments:
            mask = df['market_type'] == market_id
            df.loc[mask, 'over_line'] = line_adjustments[market_name]
            df.loc[mask, 'under_line'] = line_adjustments[market_name]
    
    return df

@pytest.fixture
def sample_processed_data() -> pd.DataFrame:
    """Create sample processed data for testing."""
    data = []
    
    # Create props for two players
    players = [
        ('Player 1', 'LAL', 'BOS'),
        ('Player 2', 'BOS', 'LAL')
    ]
    
    game_id = '2024-01-01_BOS_LAL'
    timestamp = pd.Timestamp.now()
    
    for player_name, team, opp in players:
        # Add props for each market type and sportsbook
        for market_id, market_name in MARKET_TYPES.items():
            for book_id, book_name in SPORTSBOOKS.items():
                data.append({
                    'player_name': player_name,
                    'team': team,
                    'opponent': opp,
                    'game_id': game_id,
                    'timestamp': timestamp,
                    'source': 'bettingpros',
                    'market_type': market_name,
                    'sportsbook': book_name,
                    'over_line': 20.5,  # Will be adjusted below
                    'under_line': 20.5,
                    'over_odds': -110,
                    'under_odds': -110
                })
    
    df = pd.DataFrame(data)
    
    # Adjust lines based on market type
    line_adjustments = {
        'points': 20.5,
        'rebounds': 6.5,
        'assists': 4.5,
        'three_pointers_made': 2.5,
        'steals': 1.5,
        'blocks': 1.5,
        'turnovers': 2.5,
        'points_rebounds': 27.5,
        'points_assists': 25.5,
        'rebounds_assists': 11.5,
        'points_rebounds_assists': 32.5
    }
    
    for market_name, line in line_adjustments.items():
        mask = df['market_type'] == market_name
        df.loc[mask, 'over_line'] = line
        df.loc[mask, 'under_line'] = line
    
    return df

def test_validate_raw_data(sample_raw_data):
    """Test raw data validation."""
    # Valid data should pass
    assert validate_raw_data(sample_raw_data) is True
    
    # Test missing columns
    bad_data = sample_raw_data.drop('market_type', axis=1)
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_raw_data(bad_data)
    
    # Test invalid market type
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'market_type'] = 999
    with pytest.raises(ValueError, match="Invalid market types"):
        validate_raw_data(bad_data)
    
    # Test invalid sportsbook
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'sportsbook_id'] = 999
    with pytest.raises(ValueError, match="Invalid sportsbook IDs"):
        validate_raw_data(bad_data)

def test_validate_game_data(sample_raw_data):
    """Test game data validation."""
    # Valid data should pass
    assert validate_game_data(sample_raw_data) is True
    
    # Test missing reverse matchup
    bad_data = sample_raw_data[sample_raw_data['team'] == 'LAL'].copy()
    assert validate_game_data(bad_data) is False
    
    # Test team playing itself
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'opponent'] = bad_data.loc[0, 'team']
    assert validate_game_data(bad_data) is False
    
    # Test inconsistent lines
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'over_line'] = bad_data.loc[0, 'over_line'] + 5
    assert validate_game_data(bad_data) is False

def test_validate_player_data(sample_raw_data):
    """Test player data validation."""
    # Valid data should pass
    assert validate_player_data(sample_raw_data) is True
    
    # Test low lines
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'over_line'] = 0.1
    assert validate_player_data(bad_data) is False
    
    # Test high lines
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'over_line'] = 100
    assert validate_player_data(bad_data) is False
    
    # Test extreme odds
    bad_data = sample_raw_data.copy()
    bad_data.loc[0, 'over_odds'] = -2000
    assert validate_player_data(bad_data) is False

def test_validate_output(sample_processed_data):
    """Test output validation."""
    # Valid data should pass
    assert validate_output(sample_processed_data) is True
    
    # Test missing columns
    bad_data = sample_processed_data.drop('market_type', axis=1)
    assert validate_output(bad_data) is False
    
    # Test null values
    bad_data = sample_processed_data.copy()
    bad_data.loc[0, 'team'] = None
    assert validate_output(bad_data) is False
    
    # Test timestamp format
    bad_data = sample_processed_data.copy()
    bad_data['timestamp'] = 'invalid_timestamp'
    assert validate_output(bad_data) is False 