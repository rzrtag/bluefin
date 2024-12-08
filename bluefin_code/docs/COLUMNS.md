# Column Documentation

## Overview
Documentation of all columns across data sources, including raw data columns, abbreviations, descriptions, and usage status.

## Data Merging Keys

### Primary Keys
| Key | Sources | Format | Notes |
|-----|---------|--------|-------|
| `game_id` | NBA.com | `0022300001` | Season + Game Number |
| `game_id` | SaberSim | `ssim_2023_12_01_1` | Date + Game Number |
| `game_date` | All | `YYYY-MM-DD` | Universal date format |
| `player_id` | NBA.com | `203999` | Official NBA ID |
| `player_id` | SaberSim | `ssim_203999` | Prefixed NBA ID |
| `player_name` | All | String | Requires standardization |
| `team` | All | 3-letter | Standard abbreviations |

### Standardization Rules
1. Team Abbreviations:
   - Use NBA official 3-letter codes
   - Example: `DEN`, `LAL`, `GSW`

2. Player Names:
   - Format: `First Last`
   - Remove Jr., Sr., III, etc.
   - Handle special characters

3. Dates:
   - Always `YYYY-MM-DD`
   - Store in UTC
   - Display in EST for NBA

## Metric Calculations

### Core Stats
| Metric | Formula | Source Columns | Notes |
|--------|---------|----------------|-------|
| `minutes` | `OUT_TIME - IN_TIME` | `GameRotation` | Sum per player |
| `possessions` | Custom calculation | `LineScore` | Team pace data |
| `usage_rate` | `(FGA + 0.44*FTA + TO) / POSS` | Multiple | Per-possession |

### Efficiency Metrics
| Metric | Formula | Source Columns | Notes |
|--------|---------|----------------|-------|
| `ts_pct` | `PTS / (2 * (FGA + 0.44 * FTA))` | Multiple | True Shooting % |
| `efg_pct` | `(FGM + 0.5 * FG3M) / FGA` | Multiple | Effective FG % |
| `ast_rate` | `AST / POSS` | Multiple | Per-possession |

### Prop Metrics
| Metric | Formula | Source Columns | Notes |
|--------|---------|----------------|-------|
| `win_prob` | Custom model | Multiple | Over probability |
| `ev` | `(win_prob * profit) - ((1-win_prob) * stake)` | Multiple | Expected value |
| `edge` | `win_prob - implied_prob` | Multiple | True edge |

## NBA.com Data

### BoxScoreSummaryV2

#### Summary Columns
| Column                            | Description                       | Used | Notes                    |
|----------------------------------|-----------------------------------|:----:|--------------------------|
| `GAME_ID`                        | Unique game identifier            | ✅   | Format: "0022300001"     |
| `GAME_STATUS_ID`                 | Game status code                  | ✅   | 1=Scheduled, 3=Final     |
| `GAME_STATUS_TEXT`               | Text description of game status   | ✅   | e.g., "Final"            |
| `GAMECODE`                       | Internal NBA game code            | ❌   |                          |
| `HOME_TEAM_ID`                   | Home team identifier              | ✅   | Maps to team lookup      |
| `VISITOR_TEAM_ID`                | Away team identifier              | ✅   | Maps to team lookup      |
| `SEASON`                         | Season identifier                 | ✅   | Format: "2023-24"        |
| `GAME_DATE_EST`                  | Game date in EST timezone         | ✅   | YYYY-MM-DD              |
| `LIVE_PERIOD`                    | Current game period               | ❌   | Only for live games      |
| `LIVE_PC_TIME`                   | Game clock time remaining         | ❌   | Only for live games      |
| `NATL_TV_BROADCASTER_ABBREVIATION`| TV broadcaster abbreviation      | ❌   | e.g., "ESPN", "TNT"      |
| `LIVE_PERIOD_TIME_BCAST`         | Broadcast period time             | ❌   | Only for live games      |
| `WH_STATUS`                      | Game status for wagering          | ❌   | Internal NBA use         |

#### Line Score Columns
| Column              | Description                  | Used | Notes                    |
|--------------------|------------------------------|:----:|--------------------------|
| `GAME_DATE_EST`    | Game date in EST timezone    | ✅   | YYYY-MM-DD              |
| `GAME_SEQUENCE`    | Order of game on date        | ❌   | Internal ordering        |
| `GAME_ID`          | Unique game identifier       | ✅   | Links to summary         |
| `TEAM_ID`          | Team identifier              | ✅   | Maps to team lookup      |
| `TEAM_ABBREVIATION`| Team abbreviation            | ✅   | e.g., "DEN", "LAL"       |
| `TEAM_CITY_NAME`   | Team city name              | ✅   | e.g., "Denver"           |
| `TEAM_NICKNAME`    | Team nickname               | ✅   | e.g., "Nuggets"          |
| `TEAM_WINS_LOSSES` | Team record (W-L)           | ❌   | Point-in-time record     |
| `PTS_QTR1`        | First quarter points         | ✅   | Integer                  |
| `PTS_QTR2`        | Second quarter points        | ✅   | Integer                  |
| `PTS_QTR3`        | Third quarter points         | ✅   | Integer                  |
| `PTS_QTR4`        | Fourth quarter points        | ✅   | Integer                  |
| `PTS_OT1`         | First overtime points        | ✅   | Integer, null if no OT   |
| `PTS_OT2`         | Second overtime points       | ✅   | Integer, null if no OT   |
| `PTS_OT3`         | Third overtime points        | ✅   | Integer, null if no OT   |
| `PTS_OT4`         | Fourth overtime points       | ✅   | Integer, null if no OT   |
| `PTS_OT5`         | Fifth overtime points        | ✅   | Integer, null if no OT   |
| `PTS_OT6`         | Sixth overtime points        | ✅   | Integer, null if no OT   |
| `PTS_OT7`         | Seventh overtime points      | ✅   | Integer, null if no OT   |
| `PTS_OT8`         | Eighth overtime points       | ✅   | Integer, null if no OT   |
| `PTS_OT9`         | Ninth overtime points        | ✅   | Integer, null if no OT   |
| `PTS_OT10`        | Tenth overtime points        | ✅   | Integer, null if no OT   |
| `PTS`             | Total points                 | ✅   | Sum of all periods       |

### GameRotation

| Column             | Description                  | Used | Notes                    |
|-------------------|------------------------------|:----:|--------------------------|
| `GAME_ID`         | Unique game identifier       | ✅   | Links to summary         |
| `TEAM_ID`         | Team identifier              | ✅   | Maps to team lookup      |
| `TEAM_CITY`       | Team city name              | ✅   | e.g., "Denver"           |
| `TEAM_NAME`       | Team nickname               | ✅   | e.g., "Nuggets"          |
| `PERSON_ID`       | Player identifier            | ✅   | Maps to player lookup    |
| `PLAYER_NAME`     | Player name                 | ✅   | Full name                |
| `IN_TIME_REAL`    | Entry time                  | ✅   | Format: HH:MM:SS         |
| `OUT_TIME_REAL`   | Exit time                   | ✅   | Format: HH:MM:SS         |
| `ELAPSED_TIME_REAL`| Time on court              | ✅   | Format: MM:SS            |
| `PERIOD`          | Game period (quarter)        | ✅   | 1-4, 5+ for OT          |
| `SEQUENCE`        | Order of substitution        | ✅   | Integer                  |
| `IS_HOME`         | Home/away indicator          | ✅   | Boolean                  |

## SaberSim Data

### Raw Projections
| Column         | Description                  | Used | Notes                    |
|---------------|------------------------------|:----:|--------------------------|
| `player_id`   | SaberSim player ID          | ✅   | Internal identifier      |
| `player_name` | Player name                 | ✅   | Full name                |
| `team`        | Team abbreviation           | ✅   | e.g., "DEN"              |
| `opp`         | Opponent abbreviation       | ✅   | e.g., "LAL"              |
| `game_id`     | SaberSim game ID           | ✅   | Internal identifier      |
| `date`        | Game date                   | ✅   | YYYY-MM-DD              |
| `pts`         | Points projection           | ✅   | Float                    |
| `reb`         | Rebounds projection         | ✅   | Float                    |
| `ast`         | Assists projection          | ✅   | Float                    |
| `stl`         | Steals projection           | ✅   | Float                    |
| `blk`         | Blocks projection           | ✅   | Float                    |
| `to`          | Turnovers projection        | ✅   | Float                    |
| `min`         | Minutes projection          | ✅   | Float                    |
| `fga`         | Field goal attempts         | ✅   | Float                    |
| `fgm`         | Field goals made            | ✅   | Float                    |
| `fg3a`        | Three point attempts        | ✅   | Float                    |
| `fg3m`        | Three points made           | ✅   | Float                    |
| `fta`         | Free throw attempts         | ✅   | Float                    |
| `ftm`         | Free throws made            | ✅   | Float                    |
| `off_reb`     | Offensive rebounds          | ✅   | Float                    |
| `def_reb`     | Defensive rebounds          | ✅   | Float                    |
| `pf`          | Personal fouls              | ✅   | Float                    |
| `plus_minus`  | Plus/minus projection       | ❌   | Not used for props       |
| `dk_pts`      | DraftKings points           | ❌   | DFS only                 |
| `fd_pts`      | FanDuel points              | ❌   | DFS only                 |
| `sd_pts`      | SuperDraft points           | ❌   | DFS only                 |
| `yahoo_pts`   | Yahoo points                | ❌   | DFS only                 |

### Processed Metrics
| Column         | Description                  | Used | Notes                    |
|---------------|------------------------------|:----:|--------------------------|
| `std_pts`     | Points standard deviation    | ✅   | Float                    |
| `p25_pts`     | 25th percentile points       | ✅   | Float                    |
| `p50_pts`     | Median points                | ✅   | Float                    |
| `p75_pts`     | 75th percentile points       | ✅   | Float                    |
| `p85_pts`     | 85th percentile points       | ✅   | Float                    |
| `p95_pts`     | 95th percentile points       | ✅   | Float                    |
| `p99_pts`     | 99th percentile points       | ✅   | Float                    |
| `[Similar for reb, ast, etc.]` | Percentiles for other stats | ✅ | Same format |

## BettingPros Data

### Raw Lines
| Column           | Description                  | Used | Notes                    |
|-----------------|------------------------------|:----:|--------------------------|
| `player`        | Player name                 | ✅   | Full name                |
| `team`          | Team abbreviation           | ✅   | e.g., "DEN"              |
| `opp`           | Opponent abbreviation       | ✅   | e.g., "LAL"              |
| `game_date`     | Game date                   | ✅   | YYYY-MM-DD              |
| `market`        | Market type                 | ✅   | pts, reb, ast, etc.      |
| `book`          | Sportsbook name             | ✅   | dk, fd, mgm, etc.        |
| `line`          | Over/under line             | ✅   | Float                    |
| `over_odds`     | Over odds (American)        | ✅   | Integer                  |
| `under_odds`    | Under odds (American)       | ✅   | Integer                  |
| `timestamp`     | Line update timestamp       | ✅   | UTC timestamp            |
| `consensus_line`| Consensus line              | ✅   | Float                    |
| `consensus_over`| Consensus over %            | ✅   | Float (0-100)            |
| `consensus_under`| Consensus under %          | ✅   | Float (0-100)            |
| `best_over`     | Best over odds              | ✅   | Integer                  |
| `best_under`    | Best under odds             | ✅   | Integer                  |
| `best_over_book`| Book with best over         | ✅   | Book name                |
| `best_under_book`| Book with best under       | ✅   | Book name                |

### Processed Metrics
| Column         | Description                  | Used | Notes                    |
|---------------|------------------------------|:----:|--------------------------|
| `bp_proj`     | BettingPros projection       | ✅   | Float                    |
| `bp_value`    | Value rating                 | ✅   | Integer (1-10)           |
| `bp_edge`     | Edge percentage              | ✅   | Float                    |
| `bp_consensus`| Consensus rating             | ✅   | Float (0-100)            |
| `bp_movement` | Line movement indicator      | ✅   | -1, 0, 1                 |
| `bp_steam`    | Steam move indicator         | ✅   | Boolean                  |
| `bp_sharp`    | Sharp action indicator       | ✅   | Boolean                  |

## Usage Notes
- ✅ = Currently used in analysis
- ❌ = Not currently used
- Column names preserved from source systems
- Additional derived metrics may be calculated
- All floating point numbers use standard precision
- Timestamps in UTC unless noted
- IDs map to internal lookup tables