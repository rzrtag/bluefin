# NBA Betting Strategy Guide

## Key Metrics

### Usage Rate (USG%)
Usage rate is a crucial metric that measures how often a player uses their team's possessions while on the floor. This includes:
- Field goal attempts
- Free throw attempts
- Turnovers

#### Strategic Applications
1. **Role Changes**
   - Monitor USG% changes when key players are out
   - Identify secondary players who see significant USG% increases
   - Look for value in prop markets for increased usage

2. **Matchup Analysis**
   - Compare player USG% to opponent's defensive metrics
   - Identify mismatches where high USG% players face weak defenders
   - Look for spots where USG% might increase due to matchup

3. **Lineup Impact**
   - Track USG% variations with different lineup combinations
   - Identify players who dominate usage in certain units
   - Use for live betting when specific lineups are on floor

### Efficiency Metrics

1. **True Shooting (TS%)**
   - Accounts for 2PT, 3PT, and FT efficiency
   - Compare to league average (~57%)
   - Look for sustained deviations from career norms

2. **Effective Field Goal (eFG%)**
   - Adjusts for 3PT being worth more
   - Good for projecting scoring efficiency
   - Use to identify shooting regression spots

### Advanced Playmaking

1. **Assist Rate (AST%)**
   - Percentage of teammate FGs player assists
   - Key for projecting assist props
   - Monitor changes in offensive system

2. **Rebound Rate (RB%)**
   - Percentage of available rebounds grabbed
   - Split into ORB% and DRB%
   - Crucial for rebounding props

## Market Analysis

### Props Market
1. **Line Shopping**
   - Compare lines across books
   - Look for significant discrepancies
   - Track historical pricing patterns

2. **Market Movement**
   - Monitor early line movement
   - Track steam moves
   - Identify sharp action

3. **Correlation Analysis**
   - Track related props (PTS/FGA)
   - Look for arbitrage opportunities
   - Build parlay strategies

### Live Betting
1. **Usage Monitoring**
   - Track early game usage patterns
   - Identify role changes in-game
   - Adjust projections based on flow

2. **Rotation Patterns**
   - Monitor minutes distribution
   - Track lineup combinations
   - Project second half usage

## Data-Driven Strategies

### 1. Usage Rate Edge
```python
def find_usage_opportunities(df):
    # Find players with increased usage
    baseline_usg = df.groupby('player_id')['USG'].mean()
    recent_usg = df.groupby('player_id')['USG'].last()
    
    # Look for significant increases
    usg_increase = recent_usg - baseline_usg
    opportunities = usg_increase[usg_increase > 5].index
    
    return opportunities
```

### 2. Efficiency Regression
```python
def find_regression_candidates(df):
    # Calculate rolling TS%
    df['TS_10game'] = df.groupby('player_id')['TS'].rolling(10).mean()
    df['TS_season'] = df.groupby('player_id')['TS'].transform('mean')
    
    # Look for significant deviations
    df['TS_diff'] = df['TS_10game'] - df['TS_season']
    regression_spots = df[abs(df['TS_diff']) > 0.05]
    
    return regression_spots
```

### 3. Minutes Impact
```python
def project_minutes_impact(df, out_players):
    # Get baseline minutes
    baseline_mins = df.groupby('player_id')['Min'].mean()
    
    # Calculate historical mins without key players
    impacted_mins = df[df['out_players'].isin(out_players)].groupby('player_id')['Min'].mean()
    
    # Find significant changes
    mins_impact = impacted_mins - baseline_mins
    significant_changes = mins_impact[abs(mins_impact) > 5]
    
    return significant_changes
```

## Implementation

1. **Data Pipeline**
   - Collect real-time usage data
   - Track lineup combinations
   - Monitor injury news impact

2. **Model Integration**
   - Incorporate usage into projections
   - Weight recent usage changes
   - Account for matchup factors

3. **Betting Execution**
   - Set clear criteria for plays
   - Use consistent unit sizing
   - Track results and adjust

## Key Takeaways

1. Usage rate changes provide early signal
2. Efficiency metrics help identify regression
3. Minutes and lineup data crucial for props
4. Track correlations between stats
5. Monitor live usage for in-game edges