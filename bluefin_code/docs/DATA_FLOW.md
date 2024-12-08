# Data Flow Documentation

## Overview

The Bluefin data pipeline integrates data from three main sources:
1. NBA.com (official statistics)
2. SaberSim (projections)
3. BettingPros (betting lines and props)

## NBA.com Data Pipeline

### Collection Flow
```
NBA.com API → Collectors → Raw JSON → Reorganization → Final CSV
```

### Collectors Hierarchy
1. **Game ID Collection**
   - `get_game_ids.py` fetches available game IDs
   - Filters for regular season games
   - Stores IDs in cache for reuse

2. **Main Collectors**
   - BoxScoreSummaryV2 (game metadata, teams, officials)
   - BoxScoreAdvancedV2 (advanced player stats)
   - BoxScoreFourFactorsV2 (team four factors)
   - BoxScoreScoringV2 (detailed scoring stats)
   - BoxScoreUsageV2 (usage statistics)
   - GameRotation (player substitutions)
   - PlayerGameLog (player game history)

3. **Data Organization**
   - Raw JSON stored by date/game/endpoint
   - Reorganized into CSV by endpoint type
   - Final data stored in consistent date-based structure

### Update Patterns
1. **Daily Updates** (default)
   - Looks back 3 days
   - Updates any missing or incomplete games
   
2. **Catchup Mode**
   - 30-day lookback window
   - Fills gaps in recent data

3. **Full Collection**
   - Complete season collection
   - Used for initial setup or recovery

## Data Integration

### 1. Raw Data Collection
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   NBA.com   │    │  SaberSim   │    │BettingPros  │
│  Collectors │    │   Pipeline   │    │  Scrapers   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                   │
       ▼                  ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Raw      │    │    Raw      │    │    Raw      │
│  NBA Data   │    │  Projections│    │   Props     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
```

### 2. Data Processing
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Processed  │    │  Processed  │    │  Processed  │
│  NBA Data   │    │ Projections │    │    Props    ���
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                   │
       └──────────┬──────────────────┬───────┘
                  │                  │
                  ▼                  ▼
         ┌─────────────────┐ ┌──────────────┐
         │  Merged Dataset │ │    Views     │
         └─────────────────┘ └──────────────┘
```

### Data Storage Structure
```
bluefin_data/
├── nba/
│   ├── nba_com/
│   │   ├── raw/
│   │   │   └── YYYY-MM-DD/
│   │   │       └── GAME_ID/
│   │   │           ├── boxscoresummaryv2.json
│   │   │           ├── boxscoreadvancedv2.json
│   │   │           └── ...
│   │   └── processed/
│   │       └── YYYY-MM/
│   │           ├── boxscores.csv
│   │           ├── rotations.csv
│   │           └── ...
│   ├── sabersim/
│   └── bettingpros/
└── merged/
    └── YYYY-MM/
```

## Data Refresh Patterns

### NBA.com Data
- Real-time game data updates
- 3-day rolling window for corrections
- Full season available for historical analysis

### SaberSim Data
- Daily projections updates
- Historical data preserved
- Slate-based organization

### BettingPros Data
- Multiple daily prop updates
- Multiple sportsbooks tracked
- Pre-game lines preserved

## Data Quality Checks

1. **Collection Level**
   - API response validation
   - Rate limit monitoring
   - Data completeness checks

2. **Processing Level**
   - Schema validation
   - Data type verification
   - Relationship integrity

3. **Integration Level**
   - Cross-source consistency
   - Temporal alignment
   - Key relationship validation 