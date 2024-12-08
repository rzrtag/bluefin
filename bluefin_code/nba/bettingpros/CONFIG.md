# BettingPros Configuration

This document describes the configuration and setup for the BettingPros data pipeline.

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
cd bluefin_code/nba/bettingpros
-python run.py [options]
+python run_bpro_pipeline.py [options]
```

## Running the Pipeline

The pipeline can be run in several ways:

1. Run both BettingPros and SaberSim pipelines:

```bash
cd bluefin_code/nba/bettingpros
-python run.py [options]
+python run_bpro_pipeline.py [options]
```

## Supported Sportsbooks

Traditional books processed by this pipeline:
- FanDuel (fd)
- DraftKings (dk)
- BetMGM (mgm)
- ESPN Bet (espn)

Note: PrizePicks data is now processed separately via the prizepicks module.
See bluefin_code/nba/prizepicks for details.