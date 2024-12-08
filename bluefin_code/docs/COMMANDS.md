# Bluefin Command Reference

## NBA.com Data Collection

### Main Collection Commands
```bash
# Daily collection (default) - looks back 3 days
python3 bluefin_code/nba/nba_com/collect_game.py

# Catchup collection - looks back 30 days
python3 bluefin_code/nba/nba_com/collect_game.py catchup

# Full collection - entire season(s)
python3 bluefin_code/nba/nba_com/collect_game.py full
```

### Performance Settings
Current optimal settings (in collect_game.py):
```python
# API rate limiting
RATE_LIMIT_CALLS = 1200  # 20 calls per second
RATE_LIMIT_PERIOD = 60   # Period in seconds
MIN_CALL_GAP = 0.05     # 50ms between calls

# Collection settings
CHUNK_SIZE = 10000      # Effectively no chunking
CHUNK_BREAK = 0        # No breaks between chunks
DATE_BREAK = 0         # No breaks between dates
SEASON_BREAK = 1       # 1 second between seasons
```

### Individual Collectors
```bash
# Test BoxScoreSummaryV2 collector
python3 bluefin_code/nba/nba_com/boxscoresummaryv2/collector.py

# Test GameRotation collector
python3 bluefin_code/nba/nba_com/gamerotation/collector.py
```

### Data Organization
```bash
# Fix directory structure
python3 bluefin_code/nba/nba_com/fix_structure.py

# Reorganize all data files
python3 bluefin_code/nba/nba_com/reorganize_all.py
```

## SaberSim Data Collection

### Pipeline Commands
```bash
# Run full pipeline for today
./run_pipeline.sh

# Run for specific date
./run_pipeline.sh YYYY-MM-DD

# Run for date range
./run_pipeline.sh YYYY-MM-DD YYYY-MM-DD
```

### Token Management
```bash
# Update SaberSim token
python update_config.py --token "your_new_token"

# Update slate ID
python update_config.py --slate "new_slate_id"

# Update both token and slate
python update_config.py --token "new_token" --slate "new_slate_id"
```

### Individual Commands
```bash
# Fetch projections for a specific date
python bluefin_code/nba/sabersim/fetch.py --date YYYY-MM-DD

# Process raw SaberSim data
python bluefin_code/nba/sabersim/process.py --date YYYY-MM-DD

# Force refresh existing data
python bluefin_code/nba/sabersim/fetch.py --date YYYY-MM-DD --force
```

### Batch Processing
```bash
# Process multiple dates
python bluefin_code/nba/sabersim/batch_process.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

## BettingPros Data Collection

### Fetch Single Date
```bash
# Fetch props and odds for a specific date
python bluefin_code/nba/bettingpros/fetch.py --date YYYY-MM-DD

# Force refresh existing data
python bluefin_code/nba/bettingpros/fetch.py --date YYYY-MM-DD --force

# Fetch specific sportsbook
python bluefin_code/nba/bettingpros/fetch.py --date YYYY-MM-DD --book fd
```

### Process Single Date
```bash
# Process raw BettingPros data
python bluefin_code/nba/bettingpros/process.py --date YYYY-MM-DD
```

### Batch Processing
```bash
# Process multiple dates
python bluefin_code/nba/bettingpros/batch_process.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

## Data Validation

### Validate Raw Data
```bash
# Validate SaberSim raw data
python bluefin_code/nba/sabersim/validate.py --date YYYY-MM-DD

# Validate BettingPros raw data
python bluefin_code/nba/bettingpros/validate.py --date YYYY-MM-DD
```

### Check Data Quality
```bash
# Check for missing or invalid values
python bluefin_code/nba/utils/check_quality.py --date YYYY-MM-DD --source sabersim
python bluefin_code/nba/utils/check_quality.py --date YYYY-MM-DD --source bettingpros
```

## Data Integration

### Merge Data Sources
```bash
# Merge SaberSim and BettingPros data
python bluefin_code/nba/merge.py --date YYYY-MM-DD
```

## Common Options

### Date Options
- `--date YYYY-MM-DD` - Single date
- `--start-date YYYY-MM-DD` - Start of date range
- `--end-date YYYY-MM-DD` - End of date range

### Processing Options
- `--force` - Force refresh existing data
- `--book [fd|dk|mgm|espn|pp]` - Specific sportsbook
- `--verbose` - Detailed logging output

### Output Options
- `--output-dir PATH` - Custom output directory
- `--format [csv|json]` - Output format

## Output Format

### Pipeline Output
The pipeline provides color-coded output showing:
- Team rosters (cyan)
- Key rotation players (yellow)
- Confirmed players (green)
- Injured players (red)
- Questionable/Probable players (magenta)
- Minute projections (blue)
- Status changes and updates

## Examples

### Daily Data Collection
```bash
# 1. Run SaberSim pipeline
./run_pipeline.sh

# 2. Run BettingPros collection
python bluefin_code/nba/bettingpros/fetch.py --date $(date +%Y-%m-%d)
python bluefin_code/nba/bettingpros/process.py --date $(date +%Y-%m-%d)

# 3. Merge the sources
python bluefin_code/nba/merge.py --date $(date +%Y-%m-%d)
```

### Historical Data Collection
```bash
# 1. SaberSim date range
./run_pipeline.sh 2023-11-01 2023-11-30

# 2. BettingPros date range
python bluefin_code/nba/bettingpros/batch_process.py --start-date 2023-11-01 --end-date 2023-11-30

# 3. Merge all dates
python bluefin_code/nba/merge.py --start-date 2023-11-01 --end-date 2023-11-30
```

## Directory Structure
```
bluefin_data/
├── nba/
│   ├── bettingpros/
│   │   ├── raw/
│   │   │   └── YYYY-MM/
│   │   └── processed/
│   │       └── YYYY-MM/
│   ├── sabersim/
│   │   ├── raw/
│   │   │   └── YYYY-MM/
│   │   └── processed/
│   │       └── YYYY-MM/
│   └── merged/
│       └── YYYY-MM/
└── logs/
    └── nba/
        ├── bettingpros/
        ├── sabersim/
        └── merge/
```