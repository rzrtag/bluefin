"""Core basketball metrics calculations.

This module contains standardized formulas for calculating advanced basketball metrics.
All functions expect standardized column names as defined in core/standardization.
"""

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def calculate_shooting_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate shooting efficiency metrics (TS%, eFG%)."""
    result = df.copy()
    
    # Effective Field Goal % = (FGM + 0.5 * 3PM) / FGA
    try:
        fgm = result['two_pt_made'] + result['three_pt_made']
        fga = result['two_pt_att'] + result['three_pt_att']
        result['efg_pct'] = (fgm + 0.5 * result['three_pt_made']) / fga
    except KeyError as e:
        logger.warning(f"Missing columns for eFG%: {e}")
        result['efg_pct'] = np.nan
    
    # True Shooting % = PTS / (2 * (FGA + 0.44 * FTA))
    try:
        result['ts_pct'] = result['pts'] / (2 * (fga + 0.44 * result['fta']))
    except KeyError as e:
        logger.warning(f"Missing columns for TS%: {e}")
        result['ts_pct'] = np.nan
    
    return result

def calculate_usage_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate usage rate metrics."""
    result = df.copy()
    
    # Usage Rate = (FGA + 0.44 * FTA + TOV) / (Minutes * (Team FGA + 0.44 * Team FTA + Team TOV) / (Team Minutes / 5))
    # Note: Using simplified version since we don't have team stats
    try:
        fga = result['two_pt_att'] + result['three_pt_att']
        result['usg_pct'] = (fga + 0.44 * result['fta'] + result['tov']) / result['min']
        result['usg_pct'] = result['usg_pct'] / result['usg_pct'].mean()  # Normalize to league average
    except KeyError as e:
        logger.warning(f"Missing columns for Usage Rate: {e}")
        result['usg_pct'] = np.nan
    
    return result

def calculate_assist_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate assist-related metrics."""
    result = df.copy()
    
    # Assist Rate = Assists / (Minutes * (Team FGM) / (Team Minutes / 5))
    # Note: Using simplified version since we don't have team stats
    try:
        fgm = result['two_pt_made'] + result['three_pt_made']
        result['ast_pct'] = result['ast'] / (result['min'] * fgm / 5)
    except KeyError as e:
        logger.warning(f"Missing columns for Assist Rate: {e}")
        result['ast_pct'] = np.nan
    
    return result

def calculate_rebound_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate rebounding metrics."""
    result = df.copy()
    
    try:
        # Total Rebound Rate
        result['reb_pct'] = result['reb'] / (result['min'] * (result['oreb'] + result['dreb']) / 5)
        
        # Offensive Rebound Rate
        result['oreb_pct'] = result['oreb'] / (result['min'] * result['oreb'] / 5)
        
        # Defensive Rebound Rate
        result['dreb_pct'] = result['dreb'] / (result['min'] * result['dreb'] / 5)
    except KeyError as e:
        logger.warning(f"Missing columns for Rebound Rates: {e}")
        result['reb_pct'] = np.nan
        result['oreb_pct'] = np.nan
        result['dreb_pct'] = np.nan
    
    return result

def calculate_all_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all advanced metrics."""
    result = df.copy()
    
    # Calculate each set of metrics
    result = calculate_shooting_efficiency(result)
    result = calculate_usage_rates(result)
    result = calculate_assist_rates(result)
    result = calculate_rebound_rates(result)
    
    # Clean up any infinite or NaN values
    result = result.replace([np.inf, -np.inf], np.nan)
    
    # Clip percentage metrics to valid ranges
    pct_columns = ['efg_pct', 'ts_pct', 'usg_pct', 'ast_pct', 'reb_pct', 'oreb_pct', 'dreb_pct']
    for col in pct_columns:
        if col in result.columns:
            result[col] = result[col].clip(0, 1)
    
    return result 