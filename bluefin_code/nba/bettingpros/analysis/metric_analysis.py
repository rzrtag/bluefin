#!/usr/bin/env python3

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"

SAMPLE_DATES = [
    "2024-12-05",
    "2024-12-06"
]

def load_sample_data(date: str) -> pd.DataFrame:
    """Load BettingPros data for analysis"""
    year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
    file_path = DATA_ROOT / "nba" / "bettingpros" / "processed" / year_month / f"props_{date}.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"No data file found for date: {date}")
        
    return pd.read_csv(file_path)

def analyze_single_bet(row):
    """Deep analysis of a single bet's metrics"""
    print(f"\nDetailed Analysis for {row['player']} {row['prop_type']} {row['line']}")
    
    # Convert odds to probabilities
    over_prob = 1 / (1 + (-row['over_odds']/100 if row['over_odds'] < 0 else 100/row['over_odds']))
    under_prob = 1 / (1 + (-row['under_odds']/100 if row['under_odds'] < 0 else 100/row['under_odds']))
    
    print(f"Odds Analysis:")
    print(f"Over {row['over_odds']}: {over_prob:.3f} implied probability")
    print(f"Under {row['under_odds']}: {under_prob:.3f} implied probability")
    print(f"Vig: {((over_prob + under_prob) - 1) * 100:.1f}%")
    
    print(f"\nBettingPros Projections:")
    print(f"Projected Probability: {row['projected_probability']:.3f}")
    print(f"Projected EV: {row['projected_ev']:.3f}")
    print(f"Bet Rating: {row['bet_rating']}")
    
    # Try to reverse engineer EV calculation
    stake = 1.0
    if row['over_odds'] > 0:
        potential_win = stake * (row['over_odds']/100)
    else:
        potential_win = stake * (100/abs(row['over_odds']))
        
    calc_ev = row['projected_probability'] * potential_win - (1 - row['projected_probability']) * stake
    
    print(f"\nEV Calculation Analysis:")
    print(f"Potential Win: ${potential_win:.2f} on ${stake:.2f} stake")
    print(f"Calculated EV: {calc_ev:.3f}")
    print(f"Difference from BettingPros EV: {abs(calc_ev - row['projected_ev']):.3f}")

def analyze_metrics(df: pd.DataFrame) -> None:
    """Analyze key betting metrics from sample data"""
    
    # Get high rated bets for deep analysis
    high_rated = df[
        (df['projected_ev'].notna()) & 
        (df['bet_rating'].notna())
    ].sort_values('bet_rating', ascending=False).head(3)
    
    print("\nHigh Bet Rating Examples:")
    print(high_rated[['player', 'prop_type', 'line', 'over_odds', 'under_odds',
                      'projected_value', 'projected_probability', 'projected_ev', 
                      'bet_rating']])
    
    # Deep analysis of top rated bets
    for _, row in high_rated.iterrows():
        analyze_single_bet(row)
    
    # Statistical analysis
    print("\nMetric Correlations:")
    corr = df[['projected_probability', 'projected_ev', 'bet_rating']].corr()
    print(corr)
    
    # Distribution analysis
    print("\nMetric Distributions:")
    for metric in ['projected_probability', 'projected_ev', 'bet_rating']:
        print(f"\n{metric}:")
        print(df[metric].describe())

def main():
    for date in SAMPLE_DATES:
        print(f"\nAnalyzing {date}:")
        try:
            df = load_sample_data(date)
            analyze_metrics(df)
        except FileNotFoundError:
            print(f"No data found for {date}")

if __name__ == "__main__":
    main() 