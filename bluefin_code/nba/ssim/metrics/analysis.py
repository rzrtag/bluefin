#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, List
from .evaluation import calculate_win_probability, calculate_ev, calculate_bet_rating

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "bluefin_data"

def get_ssim_projection(ssim_row: pd.Series, prop_type: str) -> float:
    """Get the correct projection value based on prop type"""
    # Clean prop type - remove any trailing numbers or whitespace
    prop_type = prop_type.strip().lower()
    prop_type = ''.join([c for c in prop_type if not c.isdigit()]).strip()
    
    # Map betting prop types to SaberSim stat columns
    prop_map = {
        # Basic stats
        'pts': 'points',
        'points': 'points',
        'reb': 'rebounds',
        'rebounds': 'rebounds',
        'ast': 'assists',
        'assists': 'assists',
        'blk': 'blocks',
        'blocks': 'blocks',
        'stl': 'steals',
        'steals': 'steals',
        'to': 'turnovers',
        'turnovers': 'turnovers',
        'threes': 'three_pt_fg',
        'threesm': 'three_pt_fg',
        'threesa': 'three_pt_attempts',
        '3pm': 'three_pt_fg',
        'threepointers': 'three_pt_fg',
        'three_pointers': 'three_pt_fg',
        'three_point': 'three_pt_fg',
        'three_points': 'three_pt_fg',
        'three_point_field_goals': 'three_pt_fg',
        'three_pt_fg': 'three_pt_fg',
        'fgm': lambda x: float(x['three_pt_fg']) + float(x['two_pt_fg']),
        'fga': lambda x: float(x['three_pt_attempts']) + float(x['two_pt_attempts']),
        'ftm': 'free_throws_made',
        'fta': 'free_throw_attempts',
        
        # Combo stats - use direct columns where available
        'pa': 'points_assists',  # Direct column
        'pr': 'points_rebounds',  # Direct column
        'ra': 'rebounds_assists',  # Direct column
        'pra': 'points_rebounds_assists',  # Direct column
        'pm': lambda x: float(x['points']),  # Points match - same as points
        'stocks': 'stocks',  # Direct column
        'dreb': 'defensive_rebounds',
        'oreb': 'offensive_rebounds',
        
        # Additional stats
        'dd': 'double_doubles',  # Double-doubles
        'td': 'triple_doubles',  # Triple-doubles
        'pf': 'fouls',  # Personal fouls
        'min': 'minutes',  # Minutes played
        
        # Percentage stats (calculated)
        'fg_pct': lambda x: (float(x['three_pt_fg']) + float(x['two_pt_fg'])) / (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) * 100 if (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) > 0 else 0,
        'three_pt_pct': lambda x: float(x['three_pt_fg']) / float(x['three_pt_attempts']) * 100 if float(x['three_pt_attempts']) > 0 else 0,
        'ft_pct': lambda x: float(x['free_throws_made']) / float(x['free_throw_attempts']) * 100 if float(x['free_throw_attempts']) > 0 else 0,
        
        # Usage metrics
        'usg': lambda x: (
            ((float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) + 
             (float(x['free_throw_attempts']) * 0.44) + 
             float(x['turnovers'])) / float(x['possessions']) * 100
        ) if float(x['possessions']) > 0 else 0,
        'usage': lambda x: get_ssim_projection(x, 'usg'),  # Alias
        'usage_rate': lambda x: get_ssim_projection(x, 'usg'),  # Alias
        
        # Per-minute rates
        'pts_per_min': lambda x: float(x['points']) / float(x['minutes']) if float(x['minutes']) > 0 else 0,
        'reb_per_min': lambda x: float(x['rebounds']) / float(x['minutes']) if float(x['minutes']) > 0 else 0,
        'ast_per_min': lambda x: float(x['assists']) / float(x['minutes']) if float(x['minutes']) > 0 else 0,
        'stl_per_min': lambda x: float(x['steals']) / float(x['minutes']) if float(x['minutes']) > 0 else 0,
        'blk_per_min': lambda x: float(x['blocks']) / float(x['minutes']) if float(x['minutes']) > 0 else 0,
        
        # Per-possession rates (key for pace-adjusted analysis)
        'pts_per_poss': lambda x: float(x['points']) / float(x['possessions']) if float(x['possessions']) > 0 else 0,
        'reb_per_poss': lambda x: float(x['rebounds']) / float(x['possessions']) if float(x['possessions']) > 0 else 0,
        'ast_per_poss': lambda x: float(x['assists']) / float(x['possessions']) if float(x['possessions']) > 0 else 0,
        'stl_per_poss': lambda x: float(x['steals']) / float(x['possessions']) if float(x['possessions']) > 0 else 0,
        'blk_per_poss': lambda x: float(x['blocks']) / float(x['possessions']) if float(x['possessions']) > 0 else 0,
        
        # Shooting distribution metrics
        'three_pt_rate': lambda x: float(x['three_pt_attempts']) / (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) * 100 if (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) > 0 else 0,
        'ft_rate': lambda x: float(x['free_throw_attempts']) / (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) if (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) > 0 else 0,
        
        # Efficiency metrics
        'ts_pct': lambda x: (
            float(x['points']) / (2 * (float(x['three_pt_attempts']) + float(x['two_pt_attempts']) + 0.44 * float(x['free_throw_attempts']))) * 100
            if (float(x['three_pt_attempts']) + float(x['two_pt_attempts']) + 0.44 * float(x['free_throw_attempts'])) > 0 else 0
        ),
        'efg_pct': lambda x: (
            (float(x['three_pt_fg']) + float(x['two_pt_fg']) + 0.5 * float(x['three_pt_fg'])) / (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) * 100
            if (float(x['three_pt_attempts']) + float(x['two_pt_attempts'])) > 0 else 0
        ),
        
        # Offensive involvement metrics
        'scoring_poss': lambda x: (
            float(x['three_pt_fg']) + float(x['two_pt_fg']) + 
            (1 - ((1 - (float(x['free_throws_made']) / float(x['free_throw_attempts']))) ** 2)) * float(x['free_throw_attempts']) * 0.44
        ) if float(x['free_throw_attempts']) > 0 else float(x['three_pt_fg']) + float(x['two_pt_fg']),
        
        # Workload metrics
        'min_per_game': lambda x: float(x['minutes']),  # Already per game in SaberSim
        'poss_per_game': lambda x: float(x['possessions']),  # Already per game in SaberSim
        
        # Versatility metrics
        'ast_to_ratio': lambda x: float(x['assists']) / float(x['turnovers']) if float(x['turnovers']) > 0 else float(x['assists']),
        'reb_rate': lambda x: float(x['rebounds']) / float(x['possessions']) * 100 if float(x['possessions']) > 0 else 0,
        'ast_rate': lambda x: float(x['assists']) / float(x['possessions']) * 100 if float(x['possessions']) > 0 else 0,
        'stl_rate': lambda x: float(x['steals']) / float(x['possessions']) * 100 if float(x['possessions']) > 0 else 0,
        'blk_rate': lambda x: float(x['blocks']) / float(x['possessions']) * 100 if float(x['possessions']) > 0 else 0,
        'to_rate': lambda x: float(x['turnovers']) / float(x['possessions']) * 100 if float(x['possessions']) > 0 else 0,
    }
    
    try:
        if prop_type in prop_map:
            if callable(prop_map[prop_type]):
                projection = prop_map[prop_type](ssim_row)
            else:
                col = prop_map[prop_type]
                if col not in ssim_row:
                    raise KeyError(f"Column {col} not found in data")
                projection = float(ssim_row[col])
            
            # Validate projection
            if not isinstance(projection, (int, float)):
                raise ValueError(f"Invalid projection type: {type(projection)}")
            if projection < 0:
                raise ValueError(f"Negative projection: {projection}")
                
            return projection
        else:
            raise KeyError(f"Unknown prop type: {prop_type}")
            
    except Exception as e:
        print(f"Warning: Error getting projection for {prop_type}: {str(e)}")
        return 0.0

def load_comparison_data(date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load both SaberSim and BettingPros data for comparison"""
    # Load BettingPros data
    year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
    bpros_file = DATA_ROOT / "nba" / "bettingpros" / "processed" / year_month / f"props_{date}.csv"
    bpros_df = pd.read_csv(bpros_file)
    
    # Load SaberSim data
    ssim_file = DATA_ROOT / "nba" / "ssim" / "processed" / year_month / f"ssim_{date}.csv"
    ssim_df = pd.read_csv(ssim_file)
    
    return ssim_df, bpros_df

def analyze_metric_comparison(ssim_row: pd.Series, bpros_row: pd.Series) -> None:
    """Compare our calculated metrics with BettingPros for a single prop"""
    # Get correct projection for prop type
    projection = get_ssim_projection(ssim_row, bpros_row['prop_type'])
    
    # Calculate our metrics
    prob = calculate_win_probability(projection, bpros_row['line'])
    ev = calculate_ev(prob, bpros_row['over_odds'])
    rating = calculate_bet_rating(ev, prob)
    
    print(f"\nAnalyzing {bpros_row['player']} {bpros_row['prop_type'].upper()} {bpros_row['line']}")
    print(f"SaberSim Projection: {projection:.1f}")
    
    print("\nOur Calculations:")
    print(f"Win Probability: {prob:.3f}")
    print(f"Expected Value: {ev:.3f}")
    print(f"Bet Rating: {rating}")
    
    print("\nBettingPros Values:")
    print(f"Win Probability: {bpros_row['projected_probability']:.3f}")
    print(f"Expected Value: {bpros_row['projected_ev']:.3f}")
    print(f"Bet Rating: {bpros_row['bet_rating']}")
    
    print("\nDifferences:")
    prob_diff = abs(bpros_row['projected_probability'] - prob)
    ev_diff = abs(bpros_row['projected_ev'] - ev)
    rating_diff = abs(bpros_row['bet_rating'] - rating)
    print(f"Probability Diff: {prob_diff:.3f}")
    print(f"EV Diff: {ev_diff:.3f}")
    print(f"Rating Diff: {rating_diff}")

def analyze_all_props(ssim_df: pd.DataFrame, bpros_df: pd.DataFrame) -> None:
    """Analyze all props in the dataset"""
    # Store metrics for distribution analysis
    our_metrics = []
    bpros_metrics = []
    
    # Map BettingPros prop types to our internal types
    prop_type_map = {
        'BLK': 'blocks',
        'TO': 'turnovers',
        'AST': 'assists',
        'REB': 'rebounds',
        'PTS': 'points',
        'STL': 'steals',
        'THREESM': 'three_pt_fg',
        '3PM': 'three_pt_fg',
        'THREES': 'three_pt_fg',
        'THREE_PT_FG': 'three_pt_fg',
        'PRA': 'pra',
        'PA': 'pa',
        'PR': 'pr',
        'RA': 'ra',
        'STOCKS': 'stocks',
        'DREB': 'dreb',
        'OREB': 'oreb',
        'FGM': 'fgm',
        'FGA': 'fga',
        'FTM': 'ftm',
        'FTA': 'fta',
    }
    
    for _, bpros_row in bpros_df.iterrows():
        if bpros_row['player'] in ssim_df['name'].values:
            ssim_row = ssim_df[ssim_df['name'] == bpros_row['player']].iloc[0]
            
            # Map BettingPros prop type to our internal type
            prop_type = prop_type_map.get(bpros_row['prop_type'].upper(), bpros_row['prop_type'].lower())
            
            # Get correct projection for prop type
            projection = get_ssim_projection(ssim_row, prop_type)
            
            # Skip if we couldn't get a valid projection
            if projection == 0.0:
                continue
            
            # Calculate our metrics
            prob = calculate_win_probability(projection, bpros_row['line'])
            ev = calculate_ev(prob, bpros_row['over_odds'])
            rating = calculate_bet_rating(ev, prob)
            
            # Print individual prop analysis
            print(f"\n{bpros_row['player']} {bpros_row['prop_type'].upper()} (Line: {bpros_row['line']:.1f})")
            print(f"SaberSim Proj: {projection:.1f} | Prob: {prob:.3f} | EV: {ev:.3f} | Rating: {rating}")
            print(f"BettingPros:   {bpros_row['projected_probability']:.3f} | EV: {bpros_row['projected_ev']:.3f} | Rating: {int(bpros_row['bet_rating'])}")
            
            # Store metrics for distribution analysis
            our_metrics.append({
                'probability': prob,
                'ev': ev,
                'rating': rating
            })
            
            bpros_metrics.append({
                'projected_probability': bpros_row['projected_probability'],
                'projected_ev': bpros_row['projected_ev'],
                'bet_rating': bpros_row['bet_rating']
            })
    
    if our_metrics:
        # Convert to DataFrames for analysis
        our_df = pd.DataFrame(our_metrics)
        bpros_df = pd.DataFrame(bpros_metrics)
        
        print("\nMetric Distributions:")
        print("\nOur Metrics:")
        print(our_df.describe().round(3))
        print("\nBettingPros Metrics:")
        print(bpros_df.describe().round(3))
    else:
        print("\nNo matching props found for analysis")

def get_dates_to_analyze() -> List[str]:
    """Get list of dates to analyze"""
    return [
        "2024-12-05",
        "2024-12-06"
    ]

def main():
    """Main entry point for analysis"""
    # Get list of dates to analyze
    dates = get_dates_to_analyze()
    
    for date in dates:
        print(f"\nAnalyzing {date}:")
        try:
            ssim_df, bpros_df = load_comparison_data(date)
            analyze_all_props(ssim_df, bpros_df)
        except FileNotFoundError:
            print(f"No data found for {date}")
        except Exception as e:
            print(f"Error analyzing {date}: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main() 