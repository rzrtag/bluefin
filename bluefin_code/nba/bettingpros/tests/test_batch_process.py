"""Test batch processing functions for BettingPros data."""

import pytest
from pathlib import Path
import json
import pandas as pd
from datetime import datetime

from ..batch_process import (
    load_raw_data,
    save_processed_data,
    process_file,
    batch_process
)

@pytest.fixture
def sample_raw_data():
    """Create sample raw data for testing."""
    return [
        {
            "participant": {"name": "Player 1"},
            "market_id": 151,  # points
            "over": {"line": 20.5, "odds": -110},
            "under": {"line": 20.5, "odds": -110},
            "_metadata": {"last_updated": "2024-01-01T12:00:00"},
            "event_id": "2024-01-01_LAL_BOS"
        },
        {
            "participant": {"name": "Player 2"},
            "market_id": 152,  # rebounds
            "over": {"line": 6.5, "odds": -110},
            "under": {"line": 6.5, "odds": -110},
            "_metadata": {"last_updated": "2024-01-01T12:00:00"},
            "event_id": "2024-01-01_LAL_BOS"
        }
    ]

@pytest.fixture
def temp_raw_file(tmp_path, sample_raw_data):
    """Create a temporary raw data file."""
    file_path = tmp_path / "raw_data.json"
    with open(file_path, 'w') as f:
        json.dump(sample_raw_data, f)
    return file_path

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "processed"
    output_dir.mkdir()
    return output_dir

def test_load_raw_data(temp_raw_file):
    """Test loading raw data from file."""
    df = load_raw_data(temp_raw_file)
    
    assert len(df) == 2
    assert 'player_name' in df.columns
    assert 'market_type' in df.columns
    assert 'over_line' in df.columns
    assert 'under_line' in df.columns
    assert 'over_odds' in df.columns
    assert 'under_odds' in df.columns
    assert 'timestamp' in df.columns
    assert 'game_id' in df.columns

def test_save_processed_data(temp_output_dir):
    """Test saving processed data to file."""
    df = pd.DataFrame({
        'player_name': ['Player 1'],
        'market_type': ['points'],
        'over_line': [20.5],
        'under_line': [20.5],
        'over_odds': [-110],
        'under_odds': [-110],
        'timestamp': [pd.Timestamp.now()],
        'game_id': ['2024-01-01_LAL_BOS']
    })
    
    output_path = temp_output_dir / "processed.json"
    save_processed_data(df, output_path)
    
    assert output_path.exists()
    with open(output_path, 'r') as f:
        saved_data = json.load(f)
    assert len(saved_data) == 1
    assert saved_data[0]['player_name'] == 'Player 1'

def test_process_file(temp_raw_file, temp_output_dir):
    """Test processing a single file."""
    output_path = temp_output_dir / "processed.json"
    process_file(temp_raw_file, output_path)
    
    assert output_path.exists()
    with open(output_path, 'r') as f:
        processed_data = json.load(f)
    
    assert len(processed_data) == 2
    assert processed_data[0]['market_type'] == 'points'
    assert processed_data[1]['market_type'] == 'rebounds'

def test_batch_process(tmp_path):
    """Test batch processing multiple files."""
    # Create input directory with multiple files
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    output_dir = tmp_path / "processed"
    
    # Create two sample files
    sample_data = [
        {
            "participant": {"name": "Player 1"},
            "market_id": 151,
            "over": {"line": 20.5, "odds": -110},
            "under": {"line": 20.5, "odds": -110},
            "_metadata": {"last_updated": "2024-01-01T12:00:00"},
            "event_id": "2024-01-01_LAL_BOS"
        }
    ]
    
    for i in range(2):
        with open(input_dir / f"raw_{i}.json", 'w') as f:
            json.dump(sample_data, f)
    
    # Run batch process
    success, errors = batch_process(input_dir, output_dir)
    
    assert success == 2
    assert errors == 0
    assert len(list(output_dir.glob('*.json'))) == 2 