# SaberSim NBA Pipeline

Pipeline for fetching and processing NBA player projections from SaberSim.

## Setup

1. Ensure you have a valid `ssim_token.yaml` in the project root:

```yaml
token: "your_token_here"
slate_id: "your_slate_id"
token_expires: "2024-01-31 23:59:59"  # Optional
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The pipeline can be run in three ways:

1. Process today's data:

```bash
./run_ssim_pipeline.sh
```

2. Process a specific date:

```bash
./run_ssim_pipeline.sh 2024-01-05
```

3. Process a date range:

```bash
./run_ssim_pipeline.sh 2024-01-01 2024-01-05
```

## Output

Data is saved in the following structure:
```
bluefin_data/
└── nba/
    └── ssim/
        ├── raw/
        │   └── 2024-01/
        │       └── NBA_2024-01-05_raw.json
        └── processed/
            └── 2024-01/
                └── ssim_2024-01-05.csv
```

## Features

- Rate-limited API requests
- Retry logic with exponential backoff
- Data validation and standardization
- Advanced metrics calculation
- Beautiful progress tracking
- Comprehensive logging

## Configuration

Configuration files in `config/`:
- `config.yaml`: API settings and request configuration
- `columns.yaml`: Data structure and column definitions
- `mappings.yaml`: Team codes and name standardization 