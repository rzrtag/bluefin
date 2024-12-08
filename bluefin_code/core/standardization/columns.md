# Core Column Standards

This document defines the standard column structure for all NBA prop data processing.
All column names follow the abbreviation standards defined in `abbreviations.md`.

## Required Base Columns

| Column Name | Type    | Description                    | Example        |
|------------|---------|--------------------------------|----------------|
| plyr       | string  | Player full name               | "LeBron James" |
| team       | string  | Team code                      | "LAL"          |
| game_id    | string  | Unique game identifier         | "20231205LAL"  |
| ts         | string  | ISO timestamp                  | "2023-12-05T..."| 

## Market Columns

| Column Name | Type    | Description                    | Example        |
|------------|---------|--------------------------------|----------------|
| mkt_type   | string  | Market type                    | "pts"          |
| line       | float   | Prop line value               | 24.5           |
| o_odds     | int     | Over odds (American)          | -110           |
| u_odds     | int     | Under odds (American)         | -110           |
| book       | string  | Sportsbook code               | "fd"           |

## Standard Market Types

| Market Type | Description                    | Notes                |
|------------|--------------------------------|---------------------|
| pts        | Points                         | Single stat         |
| reb        | Rebounds                       | Single stat         |
| ast        | Assists                        | Single stat         |
| threes     | Three pointers made            | Single stat         |
| stl        | Steals                         | Single stat         |
| blk        | Blocks                         | Single stat         |
| tov        | Turnovers                      | Single stat         |
| pr         | Points + Rebounds              | Combined stat       |
| pa         | Points + Assists               | Combined stat       |
| ra         | Rebounds + Assists             | Combined stat       |
| pra        | Points + Rebounds + Assists    | Combined stat       |

## Standard Sportsbook Codes

| Code | Sportsbook  | Notes                |
|------|-------------|---------------------|
| fd   | FanDuel     | Primary book        |
| dk   | DraftKings  | Primary book        |
| mgm  | BetMGM      | Primary book        |
| espn | ESPN Bet    | Primary book        |
| pp   | PrizePicks  | Props only          |
| ud   | Underdog    | Props only          |

## Optional Projection Columns

| Column Name | Type    | Description                    | Example        |
|------------|---------|--------------------------------|----------------|
| proj       | float   | Base projection                | 25.3           |
| proj_std   | float   | Projection std deviation       | 4.2            |
| prob_o     | float   | Probability of over (0-1)      | 0.54           |
| prob_u     | float   | Probability of under (0-1)     | 0.46           |
| ev_o       | float   | Expected value of over bet     | 2.1            |
| ev_u       | float   | Expected value of under bet    | -2.1           |

## Optional Historical Columns

| Column Name  | Type    | Description                    | Example        |
|-------------|---------|--------------------------------|----------------|
| szn_avg     | float   | Season average                 | 26.4           |
| l5_avg      | float   | Last 5 games average           | 24.8           |
| l10_avg     | float   | Last 10 games average          | 25.2           |
| ytd_avg     | float   | Year to date average           | 25.7           |

## Optional Percentile Columns

| Column Name | Type    | Description                    | Example        |
|------------|---------|--------------------------------|----------------|
| p25        | float   | 25th percentile                | 20.5           |
| p50        | float   | Median (50th percentile)       | 24.5           |
| p75        | float   | 75th percentile                | 28.5           |
| p85        | float   | 85th percentile                | 30.5           |
| p95        | float   | 95th percentile                | 35.5           |

## File Naming Convention

Files should follow this naming pattern:
- Raw data: `raw_props_YYYY_MM_DD.json`
- Processed data: `props_YYYY_MM_DD.csv`
- Projections: `projections_YYYY_MM_DD.csv`

## Notes

1. All timestamps should be in ISO format with timezone
2. All team codes should use core team standardization
3. All player names should use core name standardization
4. All files should be UTF-8 encoded
5. CSV files should use comma as delimiter
6. Missing values should be represented as empty strings for strings, NULL for numbers
7. American odds format is used (-110, +150, etc.)
8. Probabilities are expressed as decimals between 0 and 1
9. All floating point numbers should use period as decimal separator