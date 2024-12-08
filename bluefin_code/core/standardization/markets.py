#!/usr/bin/env python3

from typing import Dict, Optional, Union

MARKET_TYPES = {
    # Single stats by ID
    151: "points",
    152: "rebounds",
    156: "assists",
    160: "three_pointers_made",
    162: "steals",
    335: "blocks",
    336: "turnovers",
    
    # Combined stats by ID
    157: "points_rebounds_assists",
    337: "points_rebounds",
    338: "points_assists",
    346: "rebounds_assists",
    
    # Single stats by name
    "points": "points",
    "points-scored": "points",
    "player-points": "points",
    "total-points": "points",
    "points-over-under": "points",
    
    "rebounds": "rebounds",
    "total-rebounds": "rebounds",
    "player-rebounds": "rebounds",
    "rebounds-over-under": "rebounds",
    
    "assists": "assists",
    "total-assists": "assists",
    "player-assists": "assists",
    "assists-over-under": "assists",
    
    "three-pointers-made": "three_pointers_made",
    "3-pt-made": "three_pointers_made",
    "three-point-fg": "three_pointers_made",
    "threes-made": "three_pointers_made",
    "threes-over-under": "three_pointers_made",
    "3pts-made": "three_pointers_made",
    
    "blocks": "blocks",
    "total-blocks": "blocks",
    "player-blocks": "blocks",
    "blocks-over-under": "blocks",
    
    "steals": "steals",
    "total-steals": "steals",
    "player-steals": "steals",
    "steals-over-under": "steals",
    
    "turnovers": "turnovers",
    "total-turnovers": "turnovers",
    "player-turnovers": "turnovers",
    "turnovers-over-under": "turnovers",
    
    # Combined stats by name
    "points-rebounds-assists": "points_rebounds_assists",
    "points-assists-rebounds": "points_rebounds_assists",
    "points-rebounds": "points_rebounds",
    "points-assists": "points_assists",
    "rebounds-assists": "rebounds_assists",
    "blocks-steals": "blocks_steals"
}

def normalize_market_name(market: Union[int, str]) -> Optional[str]:
    """Convert market ID or name to standard name."""
    if isinstance(market, str):
        # Convert to lowercase and replace spaces with hyphens
        market = market.lower().replace(" ", "-")
    return MARKET_TYPES.get(market)

def get_component_markets(market: str) -> list[str]:
    """Get component markets for combined stats."""
    COMPONENTS = {
        "points_rebounds": ["points", "rebounds"],
        "points_assists": ["points", "assists"],
        "rebounds_assists": ["rebounds", "assists"],
        "points_rebounds_assists": ["points", "rebounds", "assists"],
        "blocks_steals": ["blocks", "steals"]
    }
    return COMPONENTS.get(market, [market]) 