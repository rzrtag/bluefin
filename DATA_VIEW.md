# Data View Structure

## Overview
Combined view of SaberSim projections and BettingPros odds/lines.

## Source Data

### SaberSim (Projections)
Location: `bluefin_data/nba/ssim/processed/YYYY-MM/ssim_YYYY-MM-DD.csv`
Key fields:
- Player identification (name, team)
- Base stat projections (pts, reb, ast, etc)
- DK-specific projections
- Game metadata (date, opponent)

### BettingPros (Lines/Odds)
Location: `bluefin_data/nba/bettingpros/processed/YYYY-MM/YYYY-MM-DD.csv`
Key fields:
- Player identification (name, team)
- Lines and odds by book
- Market types (pts, reb, ast, etc)
- Book metadata (site, timestamp)
- BettingPros projections
- Value metrics and opportunity signals

## Merged Structure

### Key Dimensions
- Date (YYYY-MM-DD)
- Player (name standardization needed)
- Team (using standard abbreviations)
- Market (pts, reb, ast, etc)
- Book (dk, fd, mgm, etc)

### Key Metrics
1. Projections (from SaberSim)
   - Base projection
   - Standard deviation
   - Percentiles (25,50,75,85,95,99)

2. Lines/Odds (from BettingPros)
   - Over/Under line
   - Over odds
   - Under odds
   - Book-specific metadata

3. BettingPros Analysis
   - BettingPros projection
   - Value ratings
   - Edge signals
   - Consensus metrics

### Example Output Schema
```csv
date,player,team,opp,market,book,line,o_odds,u_odds,ss_proj,ss_std,ss_p25,ss_p50,ss_p75,ss_p85,ss_p95,ss_p99,bp_proj,bp_value,bp_edge
2024-12-06,Jokic,DEN,PHX,pts,dk,30.5,-110,-110,32.4,5.2,28.5,31.2,35.1,37.2,41.5,44.8,31.5,8,2.9
``` 