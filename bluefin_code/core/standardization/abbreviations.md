# Core Abbreviation Standards

## Source Types
Data source categories:
- book - Sportsbook (MGM, FD, etc)
- proj - Projection Provider (SaberSim)
- stat - Statistical Provider (NBA.com)
- agg - Aggregator (BettingPros)

## Market Types
Props and betting markets:
- pts - Points
- reb - Rebounds
- ast - Assists
- pr - Points + Rebounds
- pa - Points + Assists
- ra - Rebounds + Assists
- pra - Points + Rebounds + Assists
- stl - Steals
- blk - Blocks
- tov - Turnovers
- threes - Three Pointers Made
- dbl - Double Double
- tpl - Triple Double

## Stat Types
Types of statistical measures:
- proj - Projection
- line - Betting line
- odds - American odds
- prob - Probability
- std - Standard deviation
- pct - Percentage
- avg - Average
- p25/50/75/etc - Percentiles

## Column Name Components

### Base Components
| Full Name    | Abbreviation | Example Use   | Notes                |
|--------------|-------------|---------------|----------------------|
| player       | plyr        | plyr_name     | For player fields   |
| projection   | proj        | pts_proj      | For projections     |
| probability  | prob        | over_prob     | For probabilities   |
| timestamp    | ts          | update_ts     | For timestamps      |
| identifier   | id          | game_id       | For IDs             |
| percentage   | pct         | hit_pct       | For percentages     |
| average      | avg         | pts_avg       | For averages        |
| standard     | std         | pts_std       | For std deviation   |
| minimum      | min         | min_pts       | For minimums        |
| maximum      | max         | max_pts       | For maximums        |

### Statistics
| Full Name      | Abbreviation | Example Use   | Notes                |
|----------------|-------------|---------------|----------------------|
| points         | pts         | pts_proj      | Points scored        |
| rebounds       | reb         | reb_proj      | Total rebounds       |
| assists        | ast         | ast_proj      | Assists              |
| steals         | stl         | stl_proj      | Steals               |
| blocks         | blk         | blk_proj      | Blocks               |
| turnovers      | tov         | tov_proj      | Turnovers           |
| three_pointers | threes      | threes_proj   | 3-pointers made     |
| minutes        | min         | min_proj      | Minutes played       |
| fouls          | pf          | pf_proj       | Personal fouls       |
| field_goals    | fg          | fg_pct        | Field goals         |
| free_throws    | ft          | ft_pct        | Free throws         |

### Combined Props
| Full Name               | Abbreviation | Example Use   | Notes                |
|------------------------|-------------|---------------|----------------------|
| points_rebounds        | pr          | pr_proj       | Points + Rebounds    |
| points_assists         | pa          | pa_proj       | Points + Assists     |
| rebounds_assists       | ra          | ra_proj       | Rebounds + Assists   |
| points_rebounds_assists| pra         | pra_proj      | Pts + Reb + Ast      |
| steals_blocks         | stocks      | stocks_proj   | Steals + Blocks      |

### Betting Terms
| Full Name      | Abbreviation | Example Use   | Notes                |
|----------------|-------------|---------------|----------------------|
| over           | o           | o_line        | Over line/odds       |
| under          | u           | u_line        | Under line/odds      |
| line           | line        | pts_line      | Betting line         |
| odds           | odds        | o_odds        | American odds        |
| sportsbook     | book        | book_id       | Sportsbook           |
| market         | mkt         | mkt_type      | Market type          |

### Sportsbooks
| Full Name      | Abbreviation | Notes                |
|----------------|-------------|----------------------|
| FanDuel        | fd          | Standard code        |
| DraftKings     | dk          | Standard code        |
| BetMGM         | mgm         | Standard code        |
| ESPN Bet       | espn        | Standard code        |
| PrizePicks     | pp          | Standard code        |
| Underdog       | ud          | Standard code        |

### Time Periods
| Full Name      | Abbreviation | Example Use   | Notes                |
|----------------|-------------|---------------|----------------------|
| season         | szn         | szn_avg       | Season stats         |
| last_n_games   | ln          | l5_pts        | Last N games         |
| year_to_date   | ytd         | ytd_avg       | Year to date         |
| rolling        | roll        | roll_avg      | Rolling average      |

### Percentiles
| Full Name      | Abbreviation | Example Use   | Notes                |
|----------------|-------------|---------------|----------------------|
| percentile_25  | p25         | pts_p25       | 25th percentile      |
| percentile_50  | p50         | pts_p50       | Median               |
| percentile_75  | p75         | pts_p75       | 75th percentile      |
| percentile_85  | p85         | pts_p85       | 85th percentile      |
| percentile_95  | p95         | pts_p95       | 95th percentile      |
| percentile_99  | p99         | pts_p99       | 99th percentile      |

## Usage Rules

1. **Component Order**:
   - Base stat first (pts, reb, ast)
   - Modifier second (proj, avg, std)
   - Time period last if applicable (l5, szn)
   Example: `pts_proj_l5`

2. **Case**:
   - All lowercase for abbreviations
   - Underscores between components
   - No periods or special characters

3. **Combining Components**:
   - Use underscores between components
   - Keep order consistent
   - Example: `pts_proj_p75_l5`

4. **File Names**:
   - Use full words for clarity
   - Separate with underscores
   - Include date in YYYY-MM-DD format
   - Example: `props_2023_12_05.csv`

5. **Consistency**:
   - Use standard abbreviations across all code
   - Don't mix abbreviation styles
   - Document any new abbreviations here

## Examples

### Column Names
```python
# Good
pts_proj     # Points projection
reb_avg_l5   # Average rebounds last 5 games
pra_p75      # 75th percentile of points+rebounds+assists
o_line       # Over line
u_odds       # Under odds

# Bad
points_proj  # Use pts abbreviation
reb_average  # Use avg abbreviation
p75_pra      # Wrong order
over_line    # Use o abbreviation
under_odds   # Use u abbreviation
```

### File Names
```python
# Good
props_2023_12_05.csv
projections_2023_12.csv
percentiles_2023_q4.csv

# Bad
12_5_23_props.csv      # Wrong date format
proj_dec_2023.csv      # Use numeric month
q4_23_pct.csv         # Use full year
```

# Standard Abbreviations

## Teams
NBA team abbreviations used across all data sources:
- ATL - Atlanta Hawks
- BOS - Boston Celtics
- BKN - Brooklyn Nets
- CHA - Charlotte Hornets
- CHI - Chicago Bulls
- CLE - Cleveland Cavaliers
- DAL - Dallas Mavericks
- DEN - Denver Nuggets
- DET - Detroit Pistons
- GSW - Golden State Warriors
- HOU - Houston Rockets
- IND - Indiana Pacers
- LAC - Los Angeles Clippers
- LAL - Los Angeles Lakers
- MEM - Memphis Grizzlies
- MIA - Miami Heat
- MIL - Milwaukee Bucks
- MIN - Minnesota Timberwolves
- NOP - New Orleans Pelicans
- NYK - New York Knicks
- OKC - Oklahoma City Thunder
- ORL - Orlando Magic
- PHI - Philadelphia 76ers
- PHX - Phoenix Suns
- POR - Portland Trail Blazers
- SAC - Sacramento Kings
- SAS - San Antonio Spurs
- TOR - Toronto Raptors
- UTA - Utah Jazz
- WAS - Washington Wizards

## Positions
Basketball positions used in rosters and eligibility:
- PG - Point Guard
- SG - Shooting Guard
- SF - Small Forward
- PF - Power Forward
- C - Center
- G - Guard (PG or SG)
- F - Forward (SF or PF)
- UTIL - Utility (any position)

## Sites
Fantasy/betting sites referenced in data:
- dk - DraftKings
- fd - FanDuel
- mgm - BetMGM
- espn - ESPN Bet
- yahoo - Yahoo DFS
- pp - PrizePicks

## Status
Player status abbreviations:
- GTD - Game Time Decision
- OUT - Out
- Q - Questionable
- D - Doubtful
- P - Probable 