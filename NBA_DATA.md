# NBA Data Collection

## Overview
Collection system for NBA.com official stats covering 2023-24 and 2024-25 seasons. Features ultra-fast collection with smart caching and optimized rate limiting.

## Data Sources

### 1. NBA.com Official Stats
Location: `bluefin_data/nba/nba_com/`

#### BoxScoreSummaryV2
- Basic game information and line scores
- Quarter-by-quarter scoring
- Game status and metadata
- Raw: `boxscoresummaryv2/raw/YYYY-MM/{game_id}_{type}.csv`
- Processed: `boxscoresummaryv2/processed/YYYY-MM/{type}_{game_id}.csv`

#### GameRotation
- Player substitution data
- On/off court timing
- Quarter-by-quarter rotations
- Raw: `gamerotation/raw/YYYY-MM/{game_id}_{team}.csv`
- Processed: `gamerotation/processed/YYYY-MM/rotation_{game_id}.csv`

## Collection Modes

### 1. Daily (Default)
```bash
python3 collect_game.py
```
- Looks back 3 days
- Perfect for daily updates
- Skips existing data

### 2. Catchup
```bash
python3 collect_game.py catchup
```
- Looks back 30 days
- For catching up after gaps
- Smart caching

### 3. Full Collection
```bash
python3 collect_game.py full
```
- Processes entire seasons
- Smart caching skips existing data
- Ultra-fast collection

## Data Formats

### Summary Data
- game_id: Unique identifier
- game_status: Current game status
- game_status_text: Text description
- game_code: Internal code
- home_team_id: Home team identifier
- visitor_team_id: Away team identifier
- season: Season identifier
- game_date: Game date (YYYY-MM-DD)

### Line Score Data
- game_id: Unique identifier
- team_id: Team identifier
- team: Team abbreviation
- team_city: Team city name
- team_name: Team nickname
- points: Total points
- points_q1: First quarter points
- points_q2: Second quarter points
- points_q3: Third quarter points
- points_q4: Fourth quarter points
- points_ot{1-10}: Overtime points

### Rotation Data
- game_id: Unique identifier
- team_id: Team identifier
- team_city: Team city name
- team_name: Team nickname
- player_id: Player identifier
- player: Player name
- in_time: Entry time
- out_time: Exit time
- elapsed_time: Time on court
- quarter: Game period
- sequence: Order of substitution
- is_home: Home/away indicator

## Performance Settings

### Rate Limits
- 1200 calls per minute
- 20 calls per second
- 50ms between calls

### Collection Settings
- No chunking (10000 size)
- No breaks between chunks
- No breaks between dates
- 1s break between seasons

## Cache Strategy
- Raw data cached by month
- Processed data organized by month
- Skip logic checks for existing files
- Force fresh option available but unused
- Cache invalidation not implemented

## Error Handling
- Graceful error recovery
- Brief pause on API errors
- Continues to next game on failure
- Logs errors but doesn't retry
- No rate limit backoff needed

## Future Improvements

### Additional Endpoints
- BoxScoreTraditional
- BoxScoreAdvanced
- PlayByPlay

### Features
- Retry logic for failed requests
- Better error logging
- Cache invalidation
- Progress tracking
- Parallel collection

### Data Quality
- Validation checks
- Data completeness verification
- Automated testing
- Schema enforcement 