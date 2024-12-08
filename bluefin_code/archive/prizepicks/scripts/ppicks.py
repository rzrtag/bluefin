#!/usr/bin/env python3

from pathlib import Path
from typing import Optional
import pandas as pd
from datetime import datetime

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"

def analyze_prizepicks(df: pd.DataFrame, output_dir: Optional[Path] = None) -> None:
    """Analyze how PrizePicks differs from other books."""
    if output_dir is None:
        output_dir = DATA_ROOT / "nba/bettingpros/analysis"
        output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"pp_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    
    pp_data = df[df['book'] == 'pp']
    other_books = [b for b in df['book'].unique() if b != 'pp']
    
    with open(output_file, 'w') as f:
        # 1. Market Coverage Analysis
        f.write("MARKET COVERAGE\n==============\n")
        pp_markets = set(pp_data['mkt'].unique())
        for book in other_books:
            book_data = df[df['book'] == book]
            book_markets = set(book_data['mkt'].unique())
            
            f.write(f"\n{book.upper()} Comparison:")
            f.write(f"\n- PP Only: {sorted(pp_markets - book_markets)}")
            f.write(f"\n- {book.upper()} Only: {sorted(book_markets - pp_markets)}")
            f.write(f"\n- Common: {sorted(pp_markets & book_markets)}\n")
        
        # 2. Line/Odds Analysis
        f.write("\n\nLINE & ODDS ANALYSIS\n===================\n")
        for book in other_books:
            book_data = df[df['book'] == book]
            f.write(f"\nPrizePicks vs {book.upper()}\n")
            
            # Compare common props
            common_players = set(pp_data['plyr']) & set(book_data['plyr'])
            line_diffs = []
            odds_diffs = []
            
            for plyr in sorted(common_players):
                pp_props = pp_data[pp_data['plyr'] == plyr]
                book_props = book_data[book_data['plyr'] == plyr]
                
                for mkt in sorted(set(pp_props['mkt']) & set(book_props['mkt'])):
                    pp_prop = pp_props[pp_props['mkt'] == mkt].iloc[0]
                    book_prop = book_props[book_props['mkt'] == mkt].iloc[0]
                    
                    line_diff = pp_prop['line'] - book_prop['line']
                    odds_diff = pp_prop['o_odds'] - book_prop['o_odds']
                    
                    line_diffs.append(line_diff)
                    odds_diffs.append(odds_diff)
                    
                    # Only show significant differences
                    if abs(line_diff) > 0.5 or abs(odds_diff) > 15:
                        f.write(
                            f"{plyr:<20} {mkt:<4} "
                            f"line: {pp_prop['line']:>4.1f} vs {book_prop['line']:>4.1f} ({line_diff:>+4.1f}) | "
                            f"odds: {pp_prop['o_odds']:>4} vs {book_prop['o_odds']:>4} ({odds_diff:>+4})\n"
                        )
            
            # Summary statistics
            if line_diffs:
                f.write(f"\nSummary Stats:")
                f.write(f"\n- Avg Line Diff: {sum(line_diffs)/len(line_diffs):+.2f}")
                f.write(f"\n- Avg Odds Diff: {sum(odds_diffs)/len(odds_diffs):+.1f}")
                f.write(f"\n- Max Line Diff: {max(abs(d) for d in line_diffs):.1f}")
                f.write(f"\n- Max Odds Diff: {max(abs(d) for d in odds_diffs)}\n")

if __name__ == "__main__":
    # Load latest data
    data_dir = DATA_ROOT / "nba/bettingpros/processed/2024-12"
    latest_file = sorted(data_dir.glob("props_*.csv"))[-1]
    df = pd.read_csv(latest_file)
    
    # Run analysis
    analyze_prizepicks(df)
    print(f"Analysis saved to: {DATA_ROOT}/nba/bettingpros/analysis/")
                            f"line: {pp_prop['line']:>4.1f} vs {book_prop['line']:>4.1f} ({line_diff:>+4.1f}) | "
                            f"odds: {pp_prop['o_odds']:>4} vs {book_prop['o_odds']:>4} ({odds_diff:>+4})\n"
                        )
            
            # Summary statistics
            if line_diffs:
                f.write(f"\nSummary Stats:")
                f.write(f"\n- Avg Line Diff: {sum(line_diffs)/len(line_diffs):+.2f}")
                f.write(f"\n- Avg Odds Diff: {sum(odds_diffs)/len(odds_diffs):+.1f}")
                f.write(f"\n- Max Line Diff: {max(abs(d) for d in line_diffs):.1f}")
                f.write(f"\n- Max Odds Diff: {max(abs(d) for d in odds_diffs)}\n")

if __name__ == "__main__":
    # Load latest data
    data_dir = DATA_ROOT / "nba/bettingpros/processed/2024-12"
    latest_file = sorted(data_dir.glob("props_*.csv"))[-1]
    df = pd.read_csv(latest_file)
    
    # Run analysis
    analyze_prizepicks(df)
    print(f"Analysis saved to: {DATA_ROOT}/nba/bettingpros/analysis/")