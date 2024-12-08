# BettingPros Data Columns

## Processed Data Columns

### Core Fields
- `plyr`: Player name (standardized)
- `team`: Team code (standardized)
- `opp`: Opponent team code (standardized)
- `game_date`: Game date (YYYY-MM-DD)
- `mkt`: Market type (standardized: PTS, REB, AST, etc.)
- `line`: Prop line value
- `o_odds`: Over odds (American)
- `u_odds`: Under odds (American)
- `book`: Sportsbook identifier (fd, dk, mgm, etc.)

### Game Context
- `game_id`: Unique game identifier
- `game_time`: Game start time
- `game_status`: Game status
- `home`: Home team code
- `away`: Away team code
- `is_home`: Whether player's team is home (boolean)

### Market Details
- `mkt_name`: Market name
- `mkt_display`: Display name
- `mkt_type`: Market type
- `mkt_category`: Market category
- `mkt_period`: Game period

### Odds/Lines
- `o_prob`: Over probability
- `u_prob`: Under probability

### Projections
- `proj_val`: Projected value
- `proj_prob`: Win probability
- `proj_edge`: Edge value
- `proj_rating`: Rating value
- `proj_conf`: Confidence level
- `proj_side`: Recommended side (over/under)

### Performance History
- `l5_avg`: Last 5 games average
- `l10_avg`: Last 10 games average
- `szn_avg`: Season average
- `home_avg`: Home games average
- `away_avg`: Away games average
- `opp_avg`: Average vs opponent

## Raw Data Structure

### Event Data
- `event_id`: Unique identifier for the game
- `sport`: Sport identifier (NBA)
- `date`: Game date
- `home_team`: Home team details
  - `name`: Team name
  - `abbreviation`: Team code
- `away_team`: Away team details
  - `name`: Team name
  - `abbreviation`: Team code

### Participant Data
- `participant`: Player information
  - `player`: Player details
    - `first_name`: First name
    - `last_name`: Last name
    - `team`: Team code
  - `name`: Full player name
  - `position`: Player position

### Market Data
- `market_id`: Type of prop bet
- `market`: Market details
  - `name`: Market name (Points, Rebounds, etc.)
  - `type`: Market type
  - `category`: Market category

### Odds/Lines
- `over`: Over bet details
  - `line`: Line value
  - `odds`: American odds
  - `probability`: Implied probability
- `under`: Under bet details
  - `line`: Line value
  - `odds`: American odds
  - `probability`: Implied probability

### Projections
- `projection`: Projection details
  - `value`: Projected value
  - `probability`: Win probability
  - `recommended_side`: Recommended bet (over/under)
  - `edge`: Edge value
  - `rating`: Rating value
  - `confidence`: Confidence level

### Performance Data
- `performance`: Historical performance
  - `last_5`: Last 5 games stats
  - `last_10`: Last 10 games stats
  - `season`: Season averages

### Metadata
- `_metadata`: Record metadata
  - `last_updated`: Timestamp
  - `update_type`: Type of update
  - `changes`: Change history

### Additional Fields
- `scoring`: Scoring rules
- `links`: Related links
- `correlated_picks`: Correlated prop bets
- `extra`: Additional information