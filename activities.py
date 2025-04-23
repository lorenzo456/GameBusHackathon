from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random

@dataclass
class Activity:
    name: str
    intensity: float
    steps: int = None
    delay: int = None
# Competitive activities - focus on measurable achievements
COMPETITIVE_ACTIVITIES = [
    Activity("Walked 10000 steps", 0.4, 10000),
    Activity("Walked 5000 steps", 0.8, 5000),
    Activity("Walked 2000 steps", 0.5, 2000),
    Activity("Walked 1000 steps", 0.6, 1000)
]

# Engagement activities - focus on social interaction
ENGAGEMENT_ACTIVITIES = [
    Activity("like_post", 0.1),
    Activity("add_comment_on_post", 0.2)
]

# Personal wellness activities - focus on self-improvement
PERSONAL_ACTIVITIES = [
    Activity("Advanced yoga flow", 0.6),
    Activity("Deep meditation", 0.2),
    Activity("Intensive strength training", 0.85),
    Activity("Skill mastery practice", 0.5),
    Activity("Recovery and mobility", 0.3),
    Activity("Advanced cardio session", 0.8),
    Activity("Mind-body connection", 0.4),
    Activity("Technical skill refinement", 0.6),
    Activity("Personal challenge workout", 0.75),
    Activity("Wellness routine", 0.4)
]

def calculate_required_intensity(goal_type: str, context: Dict[str, float]) -> float:
    """
    Calculate the required intensity for a goal based on the context.
    Higher values in context require higher intensity to achieve the goal.
    """
    base_intensity = 1.0
    
    if goal_type == "compete_with_user":
        # For competitive goals, higher competitive_score requires more intensity
        competitive_factor = context.get("competitive_score", 0.5)
        return base_intensity * (1 + competitive_factor)
    
    elif goal_type == "engage_with_user":
        # For engagement goals, lower social_score requires more intensity
        social_factor = 1 - context.get("social_score", 0.5)
        return base_intensity * (1 + social_factor)
    
    elif goal_type == "pursue_personal_goals":
        # For personal goals, higher stress requires more intensity
        stress_factor = context.get("stress_level", 0.5)
        return base_intensity * (1 + stress_factor)
    
    return base_intensity

class ActivityPlanner:
    def __init__(self, activities: List[Activity], max_activities: int = 3):
        self.activities = activities
        self.max_activities = max_activities
        self.best_solution = None
        self.best_score = float('inf')

    def _calculate_score(self, sequence: List[Activity], target_intensity: float) -> float:
        """
        Calculate how well the sequence matches the target intensity.
        Lower score is better.
        """
        total_intensity = sum(activity.intensity for activity in sequence)
        # Penalize both under and over-achieving
        return abs(total_intensity - target_intensity) + len(sequence) * 0.1

    def _backtrack(self, 
                  current_sequence: List[Activity],
                  remaining_activities: List[Activity],
                  target_intensity: float,
                  current_intensity: float) -> None:
        """
        Recursive backtracking to find the best sequence of activities.
        """
        # If we've reached the maximum number of activities or have no more activities to try
        if len(current_sequence) >= self.max_activities or not remaining_activities:
            return

        # Try each remaining activity
        for i, activity in enumerate(remaining_activities):
            new_sequence = current_sequence + [activity]
            new_intensity = current_intensity + activity.intensity
            new_remaining = remaining_activities[:i] + remaining_activities[i+1:]

            # Calculate score for this sequence
            score = self._calculate_score(new_sequence, target_intensity)

            # If this is the best solution so far, save it
            if score < self.best_score:
                self.best_solution = new_sequence
                self.best_score = score

            # If we haven't reached the target intensity, continue searching
            if new_intensity < target_intensity:
                self._backtrack(new_sequence, new_remaining, target_intensity, new_intensity)

    def find_optimal_sequence(self, target_intensity: float) -> List[Activity]:
        """
        Find the optimal sequence of activities that achieves the target intensity.
        """
        self.best_solution = None
        self.best_score = float('inf')
        
        # Start with activities sorted by intensity
        sorted_activities = sorted(self.activities, key=lambda x: x.intensity, reverse=True)
        
        # Begin backtracking search
        self._backtrack([], sorted_activities, target_intensity, 0.0)
        
        return self.best_solution or []

def select_activity(activities: List[Activity], 
                   context: Dict[str, float],
                   goal_type: str) -> List[Activity]:
    """
    Select an optimal sequence of activities that meet the goal requirements.
    """
    required_intensity = calculate_required_intensity(goal_type, context)
    planner = ActivityPlanner(activities)
    return planner.find_optimal_sequence(required_intensity) 