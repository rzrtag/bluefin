#!/usr/bin/env python3

from typing import Dict, Optional, Set

class TeamStandardizer:
    """Standardize NBA team codes and names."""
    
    # Official NBA team codes
    TEAM_CODES = {
        'ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN',
        'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
        'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX',
        'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
    }
    
    # Common variations to standard codes
    VARIATIONS = {
        'BRK': 'BKN',  # Brooklyn
        'PHO': 'PHX',  # Phoenix
        'CHS': 'CHA',  # Charlotte
        'NOR': 'NOP',  # New Orleans
        'NO': 'NOP',   # New Orleans
        'GS': 'GSW',   # Golden State
        'PHX': 'PHX',  # Phoenix (self-mapping for consistency)
        'NOP': 'NOP',  # New Orleans (self-mapping for consistency)
    }
    
    # Full team names to codes
    NAMES_TO_CODES = {
        'Atlanta Hawks': 'ATL',
        'Boston Celtics': 'BOS',
        'Brooklyn Nets': 'BKN',
        'Charlotte Hornets': 'CHA',
        'Chicago Bulls': 'CHI',
        'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL',
        'Denver Nuggets': 'DEN',
        'Detroit Pistons': 'DET',
        'Golden State Warriors': 'GSW',
        'Houston Rockets': 'HOU',
        'Indiana Pacers': 'IND',
        'Los Angeles Clippers': 'LAC',
        'Los Angeles Lakers': 'LAL',
        'Memphis Grizzlies': 'MEM',
        'Miami Heat': 'MIA',
        'Milwaukee Bucks': 'MIL',
        'Minnesota Timberwolves': 'MIN',
        'New Orleans Pelicans': 'NOP',
        'New York Knicks': 'NYK',
        'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL',
        'Philadelphia 76ers': 'PHI',
        'Phoenix Suns': 'PHX',
        'Portland Trail Blazers': 'POR',
        'Sacramento Kings': 'SAC',
        'San Antonio Spurs': 'SAS',
        'Toronto Raptors': 'TOR',
        'Utah Jazz': 'UTA',
        'Washington Wizards': 'WAS'
    }
    
    def __init__(self):
        """Initialize the standardizer."""
        # Build reverse lookup for team names
        self.codes_to_names = {v: k for k, v in self.NAMES_TO_CODES.items()}
    
    def is_valid_code(self, code: str) -> bool:
        """Check if a team code is valid."""
        if not code:
            return False
        code = code.upper()
        return code in self.TEAM_CODES or code in self.VARIATIONS
    
    def standardize_code(self, code: str) -> Optional[str]:
        """Convert team code to standard format."""
        if not code:
            return None
        code = code.upper()
        if code in self.TEAM_CODES:
            return code
        return self.VARIATIONS.get(code)
    
    def get_name(self, code: str) -> Optional[str]:
        """Get full team name from code."""
        if not code:
            return None
        code = code.upper()
        if code in self.codes_to_names:
            return self.codes_to_names[code]
        std_code = self.standardize_code(code)
        if std_code:
            return self.codes_to_names.get(std_code)
        return None
    
    def get_code(self, name: str) -> Optional[str]:
        """Get team code from full name."""
        if not name:
            return None
        return self.NAMES_TO_CODES.get(name)
    
    def validate_matchup(self, team1: str, team2: str) -> bool:
        """Validate a game matchup between two teams."""
        if not team1 or not team2:
            return False
        if not self.is_valid_code(team1) or not self.is_valid_code(team2):
            return False
        std1 = self.standardize_code(team1)
        std2 = self.standardize_code(team2)
        return std1 != std2  # Teams can't play themselves 