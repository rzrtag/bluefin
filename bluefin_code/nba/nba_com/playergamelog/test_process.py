#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

# Read raw file
raw_file = Path('/home/rzrtag/work/bluefin/bluefin_data/nba/nba_com/playergamelog/raw/2024-12/201144_2023-24.csv')
df = pd.read_csv(raw_file)

# Process data
cols = {
    'Game_ID': 'game_id',
    'GAME_DATE': 'game_date',
    'MATCHUP': 'matchup',
    'WL': 'win_loss',
    'MIN': 'minutes',
    'FGM': 'field_goals_made',
    'FGA': 'field_goals_attempted',
    'FG_PCT': 'field_goal_pct',
    'FG3M': 'three_pointers_made',
    'FG3A': 'three_pointers_attempted',
    'FG3_PCT': 'three_point_pct',
    'FTM': 'free_throws_made',
    'FTA': 'free_throws_attempted',
    'FT_PCT': 'free_throw_pct',
    'OREB': 'offensive_rebounds',
    'DREB': 'defensive_rebounds',
    'REB': 'rebounds',
    'AST': 'assists',
    'STL': 'steals',
    'BLK': 'blocks',
    'TOV': 'turnovers',
    'PF': 'personal_fouls',
    'PTS': 'points',
    'PLUS_MINUS': 'plus_minus'
}

print("\nAvailable columns:", df.columns.tolist())

# Select and rename columns
available_cols = [col for col in cols.keys() if col in df.columns]
df = df[available_cols].rename(columns={col: cols[col] for col in available_cols})

print("\nSelected columns:", df.columns.tolist())

# Convert game date
df['game_date'] = pd.to_datetime(df['game_date'], format='%b %d, %Y').dt.strftime('%Y-%m-%d')

# Convert minutes to float
def convert_minutes(x):
    if pd.isna(x) or not str(x).strip():
        return 0.0
    x_str = str(x).strip()
    if ':' in x_str:
        try:
            minutes, seconds = x_str.split(':')
            return float(minutes) + float(seconds)/60
        except:
            return 0.0
    try:
        return float(x_str)
    except:
        return 0.0

df['minutes'] = df['minutes'].apply(convert_minutes)

# Convert percentages
pct_cols = [col for col in df.columns if 'pct' in col.lower()]
for col in pct_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) / 100

print("\nProcessed data sample:")
print(df.head())

# Save processed file
processed_dir = Path('/home/rzrtag/work/bluefin/bluefin_data/nba/nba_com/playergamelog/processed/2024-12')
processed_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(processed_dir / '201144_2023-24.csv', index=False)
print('\nProcessed file saved successfully') 