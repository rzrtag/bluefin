"""
Core evaluation metrics for SaberSim projections
Matches BettingPros methodology for comparative analysis
"""

def calculate_win_probability(projection: float, line: float) -> float:
    """
    Calculate probability of projection beating the line
    
    Based on BettingPros distribution:
    - Range: 0.50 - 0.91
    - Mean: ~0.60
    - High confidence: >0.67
    """
    # Calculate edge percentage
    edge_pct = (projection - line) / line
    
    # Scale to match BettingPros distribution
    if edge_pct > 0:
        # Positive edge: 0.55 - 0.91
        prob = min(0.91, 0.55 + (edge_pct * 3))  # Increased multiplier
    else:
        # Negative edge: 0.50 - 0.55
        prob = max(0.50, 0.55 + (edge_pct * 2))
        
    return prob

def calculate_ev(probability: float, odds: int, stake: float = 1.0) -> float:
    """
    Calculate expected value using BettingPros methodology
    
    EV = (probability * potential_win) - ((1 - probability) * stake)
    """
    # Handle invalid odds
    if odds == 0:
        return 0.0
        
    if odds > 0:
        potential_win = stake * (odds/100)
    else:
        potential_win = stake * (100/abs(odds))
        
    return probability * potential_win - (1 - probability) * stake

def calculate_bet_rating(ev: float, probability: float) -> int:
    """
    Calculate 1-5 star rating based on EV and probability
    
    BettingPros patterns:
    - Strong correlation with EV (0.96)
    - Moderate correlation with probability (0.54)
    - 5★ requires: EV > 0.24 and probability > 0.67
    """
    if ev <= 0:
        return 1
        
    # Base rating on EV
    if ev > 0.30:
        base_rating = 5
    elif ev > 0.20:
        base_rating = 4
    elif ev > 0.10:
        base_rating = 3
    elif ev > 0.05:
        base_rating = 2
    else:
        base_rating = 1
        
    # Adjust for probability
    if probability < 0.60:
        base_rating = max(1, base_rating - 1)
    elif probability > 0.70:
        base_rating = min(5, base_rating + 1)
        
    return base_rating