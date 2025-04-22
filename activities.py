from typing import Dict, List
from dataclasses import dataclass
import random

@dataclass
class Activity:
    name: str
    duration: int
    steps: int = None
# Competitive activities - focus on measurable achievements
COMPETITIVE_ACTIVITIES = [
    Activity("Walked 10000 steps", 1440, 10000),
    Activity("Walked 5000 steps", 60, 5000),
    Activity("Walked 2000 steps", 10080, 2000),
    Activity("Walked 1000 steps", 2880, 1000),
]

# Engagement activities - focus on social interaction
ENGAGEMENT_ACTIVITIES = [
    Activity("like_post", 5),
    Activity("add_comment_on_post", 10)
]

# Personal wellness activities - focus on self-improvement
PERSONAL_ACTIVITIES = [
    Activity("Advanced yoga flow", 45),
    Activity("Deep meditation", 30),
    Activity("Intensive strength training", 50),
    Activity("Skill mastery practice", 40),
    Activity("Recovery and mobility", 35),
    Activity("Advanced cardio session", 45),
    Activity("Mind-body connection", 25),
    Activity("Technical skill refinement", 30),
    Activity("Personal challenge workout", 40),
    Activity("Wellness routine", 35)
]

def select_activity(activities: List[Activity], context: Dict[str, float]) -> Activity:
    """
    Select a random activity from the list.
    """
    return random.choice(activities) 