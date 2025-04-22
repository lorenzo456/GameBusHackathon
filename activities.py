from typing import Dict, List
from dataclasses import dataclass
import random

@dataclass
class Activity:
    name: str
    duration: int
    intensity: float  # 0.0 to 1.0

# Competitive activities - focus on measurable achievements
COMPETITIVE_ACTIVITIES = [
    Activity("HIIT workout", 30, 0.9),
    Activity("Running challenge", 45, 0.8),
    Activity("Strength training", 40, 0.85),
    Activity("Swimming laps", 35, 0.75),
    Activity("Cycling sprint", 25, 0.9)
]

# Engagement activities - focus on social interaction
ENGAGEMENT_ACTIVITIES = [
    Activity("like_post", 5, 0.1),
    Activity("add_comment_on_post", 10, 0.2)
]

# Personal wellness activities - focus on self-improvement
PERSONAL_ACTIVITIES = [
    Activity("Advanced yoga flow", 45, 0.6),
    Activity("Deep meditation", 30, 0.2),
    Activity("Intensive strength training", 50, 0.85),
    Activity("Skill mastery practice", 40, 0.5),
    Activity("Recovery and mobility", 35, 0.3),
    Activity("Advanced cardio session", 45, 0.8),
    Activity("Mind-body connection", 25, 0.4),
    Activity("Technical skill refinement", 30, 0.6),
    Activity("Personal challenge workout", 40, 0.75),
    Activity("Wellness routine", 35, 0.4)
]

def select_activity(activities: List[Activity], context: Dict[str, float]) -> Activity:
    """
    Select a random activity from the list.
    """
    return random.choice(activities) 