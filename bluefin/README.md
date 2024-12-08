# NBA Props Data Pipeline

A data pipeline for collecting and analyzing NBA player props data from multiple sources.

## Data Sources

### BettingPros API
- Multiple sportsbooks (FanDuel, DraftKings, BetMGM, ESPN Bet, PrizePicks)
- Player props and odds
- Historical tracking

### SaberSim
- Player projections and simulations
- Advanced stats and metrics
- Historical performance data
- Support for multiple sites (FD/DK/Yahoo)
- Automated data collection with retry logic

## Directory Structure
```
bluefin_data/
├── nba/
│   ├── bettingpros/
│   │   ├── raw/                 # Raw JSON files from API
│   │   │   └── YYYY-MM/        # Monthly directories
│   │   │       ├── date_events.json
│   │   │       ├── date_fd.json
│   │   │       ├── date_dk.json
│   │   │       ├── date_mgm.json
│   │   │       ├── date_espn.json
│   │   │       └── date_pp.json
│   │   ├── processed/           # Normalized & merged data
│   │   │   └── YYYY-MM/
│   │   │       └── date_normalized.json
│   │   └── logs/               # Log files
│   └── sabersim/
       ├── raw/                  # Raw SaberSim data
       │   └── YYYY-MM/
       │       └── date_projections.json
       ├── processed/            # Processed projections
       │   └── YYYY-MM/
       │       └── date_processed.json
       └── logs/                # Log files
```

## Configuration

### Environment Variables
```
# BettingPros API
BETTINGPROS_API_KEY=your_api_key
BETTINGPROS_API_LEVEL=your_api_level

# Request Settings
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3
RETRY_BACKOFF=1
DEBUG=True
```

### Market Types
```python
MARKET_TYPES = {
    151: "points",
    152: "rebounds",
    156: "assists",
    157: "points_rebounds_assists",
    160: "three_pointers_made",
    162: "steals",
    335: "blocks",
    336: "turnovers",
    337: "points_rebounds",
    338: "points_assists",
    346: "rebounds_assists"
}
```

### Supported Sportsbooks
| Name       | ID | Code | Description         |
|------------|------|------|-------------------|
| FanDuel    | 10   | fd   | FanDuel Sportsbook|
| DraftKings | 12   | dk   | DraftKings Sportsbook|
| BetMGM     | 19   | mgm  | BetMGM Sportsbook|
| ESPN Bet   | 33   | espn | ESPN Bet|
| PrizePicks | 37   | pp   | PrizePicks|

## Data Pipeline

### 1. Data Collection
#### BettingPros Fetch (bettingpros/fetch.py)
- Fetches raw props and odds from multiple sportsbooks
- Saves to raw/YYYY-MM/date_*.json files
- Includes validation and change detection

#### SaberSim Fetch (sabersim/fetch.py)
- Fetches player projections and advanced stats
- Supports multiple sites (FD/DK/Yahoo)
- Includes retry logic and error handling
- Saves to raw/YYYY-MM/date_projections.json

### 2. Data Processing
#### BettingPros Process (bettingpros/process.py)
- Normalizes prop data into standard format
- Merges data from all sportsbooks
- Saves to processed/YYYY-MM/date_normalized.json

#### SaberSim Process (sabersim/process.py)
- Processes raw projections data
- Standardizes player names and stats
- Saves to processed/YYYY-MM/date_processed.json

## Current Development
1. Data Integration
   - Merging BettingPros and SaberSim data
   - Player name standardization
   - Cross-source data validation

2. Analysis Tools
   - Props vs projections comparison
   - Historical performance tracking
   - Odds analysis across sportsbooks

## Next Steps
1. Complete data integration between sources
2. Implement automated testing
3. Develop visualization tools
4. Add historical analysis capabilities 