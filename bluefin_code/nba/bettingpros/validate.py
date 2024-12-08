"""Data validation functions for BettingPros data."""

import logging
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np

# Market type mapping
MARKET_TYPES = {
    151: "pts",
    152: "reb",
    156: "ast",
    157: "pra",
    160: "threes",
    162: "stl",
    335: "blk",
    336: "tov",
    337: "pr",
    338: "pa",
    346: "ra"
}

# Sportsbook mapping
SPORTSBOOKS = [
    ('FanDuel', 'fd', '10'),
    ('DraftKings', 'dk', '12'),
    ('BetMGM', 'mgm', '19'),
    ('ESPN Bet', 'espn', '33'),
]

def validate_raw_data(df: pd.DataFrame) -> bool:
    """Validate raw data format and content."""
    logger = logging.getLogger("bettingpros.validate")
    
    # Required columns
    required_cols = [
        'plyr', 'team', 'opponent', 'mkt_type',
        'book_id', 'line', 'o_odds', 'u_odds'
    ]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Valid market types
    invalid_markets = df[~df['mkt_type'].isin(MARKET_TYPES)]['mkt_type'].unique()
    if len(invalid_markets) > 0:
        raise ValueError(f"Invalid market types found: {invalid_markets}")
    
    # Valid sportsbooks
    invalid_books = df[~df['book_id'].isin(SPORTSBOOKS)]['book_id'].unique()
    if len(invalid_books) > 0:
        raise ValueError(f"Invalid sportsbook IDs found: {invalid_books}")
    
    # Log validation summary
    logger.info(f"Validated {len(df)} rows of data")
    logger.info(f"Market types: {sorted(df['mkt_type'].unique())}")
    logger.info(f"Sportsbooks: {sorted(df['book_id'].unique())}")
    
    return True

def validate_game_data(df: pd.DataFrame) -> bool:
    """Validate game-level data consistency."""
    logger = logging.getLogger("bettingpros.validate")
    validation_errors = []
    
    # Check for teams playing themselves
    self_games = df[df['team'] == df['opponent']]
    if not self_games.empty:
        for _, row in self_games.iterrows():
            validation_errors.append(
                f"Team playing itself: {row['team']} vs {row['opponent']}"
            )
    
    # Check for duplicate games
    games = df[['team', 'opponent']].drop_duplicates()
    for _, game in games.iterrows():
        reverse_game = games[
            (games['team'] == game['opponent']) & 
            (games['opponent'] == game['team'])
        ]
        if len(reverse_game) == 0:
            validation_errors.append(
                f"Missing reverse matchup for {game['team']} vs {game['opponent']}"
            )
    
    # Check for consistent lines across books
    for market in df['mkt_type'].unique():
        market_data = df[df['mkt_type'] == market]
        for _, player_data in market_data.groupby('plyr'):
            lines = player_data['line'].unique()
            if len(lines) > 1:
                max_diff = lines.max() - lines.min()
                if max_diff > 2:  # Allow small differences
                    validation_errors.append(
                        f"Large line discrepancy for {player_data.iloc[0]['plyr']} "
                        f"{MARKET_TYPES[market]}: {lines.min():.1f}-{lines.max():.1f}"
                    )
    
    if validation_errors:
        for error in validation_errors:
            logger.warning(error)
        return False
    
    return True

def validate_player_data(df: pd.DataFrame) -> bool:
    """Validate player-level data."""
    logger = logging.getLogger("bettingpros.validate")
    validation_errors = []
    
    # Check for reasonable line ranges
    line_ranges = {
        'pts': (5, 45),
        'reb': (2, 20),
        'ast': (1, 15),
        'threes': (0.5, 10),
        'stl': (0.5, 5),
        'blk': (0.5, 5),
        'tov': (0.5, 8),
        'pr': (10, 60),
        'pa': (10, 55),
        'ra': (5, 30),
        'pra': (15, 75)
    }
    
    for market_id, market_name in MARKET_TYPES.items():
        if market_name not in line_ranges:
            continue
            
        market_data = df[df['mkt_type'] == market_id]
        min_val, max_val = line_ranges[market_name]
        
        # Check low lines
        low_lines = market_data[market_data['line'] < min_val]
        if not low_lines.empty:
            for _, row in low_lines.iterrows():
                validation_errors.append(
                    f"{row['plyr']}: Low {market_name} line: {row['line']:.1f}"
                )
        
        # Check high lines
        high_lines = market_data[market_data['line'] > max_val]
        if not high_lines.empty:
            for _, row in high_lines.iterrows():
                validation_errors.append(
                    f"{row['plyr']}: High {market_name} line: {row['line']:.1f}"
                )
    
    # Check for reasonable odds ranges (-1000 to +1000)
    extreme_odds = df[
        (df['o_odds'].abs() > 1000) |
        (df['u_odds'].abs() > 1000)
    ]
    if not extreme_odds.empty:
        for _, row in extreme_odds.iterrows():
            validation_errors.append(
                f"{row['plyr']}: Extreme odds: {row['o_odds']}/{row['u_odds']}"
            )
    
    if validation_errors:
        for error in validation_errors:
            logger.warning(error)
        return False
    
    return True

def validate_output(df: pd.DataFrame) -> bool:
    """Validate final output format and content."""
    logger = logging.getLogger("bettingpros.validate")
    validation_errors = []
    
    # Check required columns
    required_cols = [
        'plyr', 'team', 'opponent', 'game_id',
        'ts', 'source', 'mkt_type', 'book',
        'line', 'o_odds', 'u_odds'
    ]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        validation_errors.append(f"Missing required columns: {missing_cols}")
    
    # Check for nulls in key columns
    for col in ['plyr', 'team', 'opponent', 'game_id']:
        if col in df.columns and df[col].isnull().any():
            null_count = df[col].isnull().sum()
            validation_errors.append(f"Found {null_count} null values in {col}")
    
    # Check data types
    if 'ts' in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df['ts']):
            validation_errors.append("ts column should be datetime type")
        else:
            # Check for invalid timestamps
            invalid_ts = df[df['ts'] <= pd.Timestamp.min]
            if not invalid_ts.empty:
                validation_errors.append(f"Found {len(invalid_ts)} invalid timestamps")
    
    # Log validation summary
    logger.info("Validation summary:")
    logger.info(f"  • {len(df)} props with complete data")
    logger.info(f"  • {len(validation_errors)} validation errors")
    if 'team' in df.columns:
        # Handle null values in sorting
        teams = sorted(t for t in df['team'].unique() if pd.notna(t))
        logger.info(f"  • Teams: {teams}")
    
    if validation_errors:
        for error in validation_errors:
            logger.error(error)
        return False
    
    return True

def validate_props_df(df: pd.DataFrame) -> List[str]:
    """Validate the props DataFrame meets requirements."""
    errors = []
    
    # Check required columns exist
    required_cols = [
        'plyr', 'team', 'opponent', 'mkt_type', 'book',
        'line', 'o_odds', 'u_odds', 'ts', 'source'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    
    # Check timestamp is datetime
    if 'ts' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['ts']):
        errors.append("ts column should be datetime type")
        
    return errors 