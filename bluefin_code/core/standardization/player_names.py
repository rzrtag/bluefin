#!/usr/bin/env python3

import re
from typing import Dict, Optional

class PlayerNameStandardizer:
    """Standardize player names across data sources."""
    
    def __init__(self):
        self.suffixes = {'Jr.', 'Sr.', 'II', 'III', 'IV'}
        self.nickname_map = {
            # Add known nicknames
            'Moe': 'Maurice',
            'PJ': 'P.J.',
            # Add more as needed
        }
    
    def remove_suffix(self, name: str) -> str:
        """Remove suffixes like Jr., III etc."""
        for suffix in self.suffixes:
            name = re.sub(f' {suffix}$', '', name)
        return name.strip()
    
    def standardize(self, name: str) -> str:
        """Convert name to standard format."""
        # Remove suffixes
        name = self.remove_suffix(name)
        
        # Handle nicknames
        parts = name.split()
        if parts[0] in self.nickname_map:
            parts[0] = self.nickname_map[parts[0]]
        
        return ' '.join(parts)
    
    def match_names(self, name1: str, name2: str) -> bool:
        """Check if two names refer to the same player."""
        std1 = self.standardize(name1)
        std2 = self.standardize(name2)
        return std1 == std2 