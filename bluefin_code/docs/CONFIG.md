# Configuration Guide

## Environment Variables

### NBA.com Collection
```bash
# Optional: Override default rate limits
NBA_RATE_LIMIT_CALLS=1200    # Calls per period (default: 1200)
NBA_RATE_LIMIT_PERIOD=60     # Period in seconds (default: 60)
NBA_MIN_CALL_GAP=0.05       # Minimum gap between calls in seconds (default: 0.05)

# Optional: Override collection settings
NBA_CHUNK_SIZE=10000        # Number of games per chunk (default: 10000)
NBA_CHUNK_BREAK=0           # Break between chunks in seconds (default: 0)
NBA_DATE_BREAK=0            # Break between dates in seconds (default: 0)
NBA_SEASON_BREAK=1          # Break between seasons in seconds (default: 1)

# Optional: Date range overrides
# 2023-24 Season
NBA_START_DATE=2023-10-24   # 2023-24 Regular season start
NBA_END_DATE=2024-04-14     # 2023-24 Regular season end

# 2024-25 Season
NBA_START_DATE=2024-10-22   # 2024-25 Regular season start
NBA_END_DATE=2025-04-13     # 2024-25 Regular season end

# Note: Dates can be overridden via command line arguments
```

### SaberSim Collection
```bash
# Required
SABERSIM_TOKEN="your_token_here"    # SaberSim API token
SABERSIM_SLATE="slate_id_here"      # Current slate ID

# Optional
SABERSIM_CACHE_TTL=3600             # Cache lifetime in seconds (default: 3600)
```

### BettingPros Collection
```bash
# Optional: Sportsbook preferences
BETTINGPROS_BOOKS=["fd","dk","mgm"] # Priority order for sportsbooks
BETTINGPROS_CACHE_TTL=1800          # Cache lifetime in seconds (default: 1800)
```

## Rate Limiting Configuration

### NBA.com API Limits
```python
# Default settings (recommended for stability)
RATE_LIMIT_CALLS = 1200    # 20 calls per second
RATE_LIMIT_PERIOD = 60     # 1 minute period
MIN_CALL_GAP = 0.05        # 50ms minimum between calls

# Aggressive settings (use with caution)
RATE_LIMIT_CALLS = 3000    # 50 calls per second
RATE_LIMIT_PERIOD = 60     # 1 minute period
MIN_CALL_GAP = 0.02        # 20ms minimum between calls

# Conservative settings (for reliability)
RATE_LIMIT_CALLS = 600     # 10 calls per second
RATE_LIMIT_PERIOD = 60     # 1 minute period
MIN_CALL_GAP = 0.1         # 100ms minimum between calls
```

## Cache Configuration

### Directory Structure
```
~/.cache/bluefin/
├── nba_com/
│   ├── game_ids/
│   │   └── YYYY-MM.json
│   └── responses/
│       └── ENDPOINT_GAME_ID.json
├── sabersim/
│   └── slates/
│       └── YYYY-MM-DD.json
└── bettingpros/
    └── props/
        └── YYYY-MM-DD.json
```

### Cache Settings
```python
# Default cache settings
CACHE_ENABLED = True           # Enable/disable caching
CACHE_BASE_DIR = "~/.cache/bluefin"
CACHE_FILE_MODE = 0o600       # Secure file permissions

# Cache lifetimes (seconds)
CACHE_TTL = {
    'game_ids': 86400,        # 24 hours
    'boxscores': 3600,        # 1 hour
    'rotations': 3600,        # 1 hour
    'sabersim': 3600,         # 1 hour
    'bettingpros': 1800       # 30 minutes
}
```

## Data Storage Configuration

### Directory Structure
```
bluefin_data/
├── nba/
│   ├── nba_com/
│   │   ├── raw/              # Raw JSON responses
│   │   └── processed/        # Processed CSV files
│   ├── sabersim/
│   │   ├── raw/
│   │   └── processed/
│   └── bettingpros/
│       ├── raw/
│       └── processed/
└── merged/                   # Integrated datasets
```

### Storage Settings
```python
# Base directories
DATA_DIR = "./bluefin_data"
RAW_DIR = f"{DATA_DIR}/raw"
PROCESSED_DIR = f"{DATA_DIR}/processed"
MERGED_DIR = f"{DATA_DIR}/merged"

# File formats
RAW_FORMAT = "json"
PROCESSED_FORMAT = "csv"
COMPRESSION = None           # Optional: "gzip" or "zip"
```

## Logging Configuration

### Log Levels
```python
# Available log levels
LOG_LEVELS = {
    'DEBUG': 10,    # Detailed debugging information
    'INFO': 20,     # General information about progress
    'WARNING': 30,  # Warnings about potential issues
    'ERROR': 40,    # Errors that don't stop execution
    'CRITICAL': 50  # Critical errors that stop execution
}

# Default settings
DEFAULT_LOG_LEVEL = 'INFO'
LOG_FILE = './bluefin.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

### Log Directory Structure
```
logs/
├── nba/
│   ├── nba_com/
│   │   └── YYYY-MM-DD.log
│   ├── sabersim/
│   │   └── YYYY-MM-DD.log
│   └── bettingpros/
│       └── YYYY-MM-DD.log
└── merged/
    └── YYYY-MM-DD.log
```

## Error Handling Configuration

### Retry Settings
```python
# Default retry configuration
MAX_RETRIES = 3              # Maximum number of retry attempts
RETRY_DELAY = 1.0           # Base delay between retries (seconds)
RETRY_BACKOFF = 2.0         # Multiplicative backoff factor
RETRY_MAX_DELAY = 30.0      # Maximum delay between retries
```

### Error Thresholds
```python
# Error tolerance settings
MAX_ERRORS_PER_DATE = 5     # Maximum errors before skipping date
MAX_ERRORS_PER_CHUNK = 3    # Maximum errors before skipping chunk
ERROR_COOLDOWN = 300        # Cooldown period after max errors (seconds)
```
``` 