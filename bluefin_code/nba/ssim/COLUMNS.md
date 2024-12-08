# SaberSim Data Columns

## Overview
CSV files containing SaberSim NBA player projections and metadata.

## Column Descriptions

### Player Information
- `name` - Player full name
- `team` - Player's team abbreviation (see [Team Abbreviations](../../core/standardization/abbreviations.md#teams))
- `opponent` - Opponent team abbreviation (see [Team Abbreviations](../../core/standardization/abbreviations.md#teams))
- `position` - Primary position (see [Position Abbreviations](../../core/standardization/abbreviations.md#positions))
- `roster_pos` - Eligible roster positions (e.g., "PG/SG", see [Position Abbreviations](../../core/standardization/abbreviations.md#positions))

### Game Information
- `date` - Game date (YYYY-MM-DD)
- `gid` - Game ID
- `pid` - Player ID
- `slate` - Slate ID
- `site` - Site identifier (see [Site Abbreviations](../../core/standardization/abbreviations.md#sites))
- `num_games` - Number of games in slate
- `timestamp` - Unix timestamp of projection

### Basic Stats Projections
- `minutes` - Projected minutes played
- `points` - Projected points scored
- `rebounds` - Total projected rebounds
- `assists` - Projected assists
- `steals` - Projected steals
- `blocks` - Projected blocks
- `turnovers` - Projected turnovers

### Aggregated Market Projections
- `points_rebounds` - Points + Rebounds total
- `points_assists` - Points + Assists total
- `rebounds_assists` - Rebounds + Assists total
- `points_rebounds_assists` - Points + Rebounds + Assists total
- `stocks` - Steals + Blocks total

### Detailed Stats Projections
- `three_pt_fg` - Projected 3-point field goals made
- `three_pt_attempts` - Projected 3-point attempts
- `two_pt_fg` - Projected 2-point field goals made
- `two_pt_attempts` - Projected 2-point attempts
- `free_throws_made` - Projected free throws made
- `free_throw_attempts` - Projected free throw attempts
- `offensive_rebounds` - Projected offensive rebounds
- `defensive_rebounds` - Projected defensive rebounds
- `fouls` - Projected personal fouls
- `possessions` - Projected possessions
- `double_doubles` - Projected double-doubles
- `triple_doubles` - Projected triple-doubles

### DraftKings Fantasy Projections
- `dk_points` - Projected DraftKings fantasy points
- `dk_std` - Standard deviation of DK points projection
- `dk_25_percentile` - 25th percentile DK points
- `dk_50_percentile` - 50th percentile DK points (median)
- `dk_75_percentile` - 75th percentile DK points
- `dk_85_percentile` - 85th percentile DK points
- `dk_95_percentile` - 95th percentile DK points
- `dk_99_percentile` - 99th percentile DK points

### Additional Fields
- `price` - Player's salary/price
- `value` - Projected value (points per dollar)
- `proj_own` - Projected ownership percentage
- `injury` - Injury status (e.g., "GTD", "OUT")
- `injury_notes` - Detailed injury information
- `injury_confirmed` - Boolean indicating if injury is confirmed
- `confirmed` - Boolean indicating if player is confirmed to play

## Example Row
```csv
date,name,team,opponent,minutes,points,...
2024-12-01,Jared McCain,PHI,CHA,22.85,15.84,3.34,1.49,...
``` 