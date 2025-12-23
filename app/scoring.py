import pandas as pd

def calculate_composite_score(views, engagement_score):
    """
    Weighted Scoring: 40% Views, 60% Active Engagement
    Normalized on a 0-100 scale.
    """
    # Simple normalization example for a single entry
    # In production, this would use Min-Max scaling across the whole DB
    score = (views * 0.4) + (engagement_score * 0.6)
    return min(100, score / 100) # Capped at 100