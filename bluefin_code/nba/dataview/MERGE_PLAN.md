# NBA Data Merge Plan

## Overview
This document outlines the plan for merging projection data from SaberSim and BettingPros sources to create a unified view for analysis.

## Data Sources

### SaberSim
- Contains player projections from SaberSim's API
- Processed data stored in: `bluefin_data/nba/ssim/processed/{year_month}/ssim_{date}.csv`
- Key metrics: points, rebounds, assists, etc.

### BettingPros
- Contains consensus betting lines and odds
- Processed data stored in: `bluefin_data/nba/bettingpros/processed/{year_month}/{date}.csv`
- Key metrics: over/under lines, odds

## Merge Strategy

### 1. Player Name Matching
- Implement fuzzy matching for player names between sources
- Create a player name mapping dictionary for edge cases
- Handle cases like "Ant Edwards" vs "Anthony Edwards"

### 2. Key Fields to Merge
- Player name
- Team
- Position
- Game date/time
- SaberSim projections
- BettingPros lines and odds

### 3. Data Quality Checks
- Verify all players from BettingPros have matching SaberSim projections
- Flag missing or mismatched data
- Validate team abbreviations are consistent

### 4. Output Format
Example merged dataframe structure:
{
    'player_name': str,
    'team': str,
    'position': str,
    'game_datetime': datetime,
    'opponent': str,
    'ssim_points': float,
    'ssim_rebounds': float,
    'ssim_assists': float,
    'bpro_points_line': float,
    'bpro_points_over_odds': float,
    'bpro_points_under_odds': float
}

## Implementation Steps

1. **Initial Setup**
   - Create test datasets
   - Set up unit tests for merge functions

2. **Core Merge Function**
   - Implement player name matching
   - Merge core fields
   - Add data validation

3. **Quality Assurance**
   - Add logging for merge issues
   - Create data quality reports
   - Track merge success rate

4. **Performance Optimization**
   - Cache player name mappings
   - Optimize merge operations

## Usage Example


## Next Steps
1. Implement basic name matching
2. Create test cases with sample data
3. Build core merge logic
4. Add validation and error handling
5. Create reporting functions for data quality

## Column Mapping Analysis

### SaberSim Columns
- player_name
- team
- position
- opponent
- game_datetime
- minutes
- points
- rebounds
- assists
- steals
- blocks
- turnovers
- three_points_made
- field_goals_made
- field_goals_attempted
- free_throws_made
- free_throws_attempted

### BettingPros Columns
- player_name
- team
- position
- opponent
- game_datetime
- prop_type (points, rebounds, assists, etc.)
- line
- over_odds
- under_odds

### Merged View Columns

#### Core Identifiers
- player (player_name)
- team (team_abbreviation)
- pos (position)
- opp (opponent)
- dt (game_datetime)

#### SaberSim Projections
Minutes & Scoring:
- ssim_min (minutes)
- ssim_pts (points)
- ssim_fgm (field_goals_made)
- ssim_fga (field_goals_attempted)
- ssim_ftm (free_throws_made)
- ssim_fta (free_throws_attempted)
- ssim_threes (three_points_made)

Stats:
- ssim_reb (rebounds)
- ssim_ast (assists)
- ssim_stl (steals)
- ssim_blk (blocks)
- ssim_tov (turnovers)

#### BettingPros Lines
Points:
- bpro_pts_line (points_line)
- bpro_pts_over (points_over_odds)
- bpro_pts_under (points_under_odds)

Rebounds:
- bpro_reb_line (rebounds_line)
- bpro_reb_over (rebounds_over_odds)
- bpro_reb_under (rebounds_under_odds)

Assists:
- bpro_ast_line (assists_line)
- bpro_ast_over (assists_over_odds)
- bpro_ast_under (assists_under_odds)

Steals:
- bpro_stl_line (steals_line)
- bpro_stl_over (steals_over_odds)
- bpro_stl_under (steals_under_odds)

Blocks:
- bpro_blk_line (blocks_line)
- bpro_blk_over (blocks_over_odds)
- bpro_blk_under (blocks_under_odds)

Three Pointers:
- bpro_threes_line (three_points_line)
- bpro_threes_over (three_points_over_odds)
- bpro_threes_under (three_points_under_odds)

### Data Type Standardization
- All player names: string, lowercase, stripped
- Teams: standardized abbreviations (using core.standardization.teams)
- Positions: standardized format (PG, SG, SF, PF, C)
- Datetime: pandas datetime objects
- Numeric values: float64
- Odds: integer (American odds format)

### Special Handling Cases
1. BettingPros prop_type needs to be pivoted to create separate columns for each prop
2. Missing props in BettingPros should be filled with NaN
3. Team abbreviations need standardization between sources
4. Game times need to be converted to consistent timezone (UTC)

### Column Abbreviations & Standardization

#### Core Abbreviations
- pts = points
- reb = rebounds
- ast = assists
- stl = steals
- blk = blocks
- tov = turnovers
- threes = three_points_made
- fgm = field_goals_made
- fga = field_goals_attempted
- ftm = free_throws_made
- fta = free_throws_attempted
- min = minutes

#### Source Prefixes
- ssim_ = SaberSim data
- bpro_ = BettingPros data

#### Suffix Conventions
- _line = prop line value
- _over = over odds
- _under = under odds

#### Examples
- ssim_pts = SaberSim points projection
- bpro_pts_line = BettingPros points line
- bpro_pts_over = BettingPros points over odds
- ssim_fga = SaberSim field goals attempted
- bpro_threes_under = BettingPros three pointers under odds

### Column Name Mapping