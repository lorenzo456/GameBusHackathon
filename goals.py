from typing import Dict, Any, List
import random

class Goal:
    def __init__(self, name: str, description: str, priority: int):
        self.name = name
        self.description = description
        self.priority = priority

class GoalManager:
    def __init__(self):
        self.goals = [
            "compete_with_user",
            "engage_with_user",
            "pursue_personal_goals"
        ]
        self.goal_weights = {
            "compete_with_user": 0.4,
            "engage_with_user": 0.3,
            "pursue_personal_goals": 0.3
        }

    def select_goal(self, user_context: Dict[str, float]) -> str:
        """
        Select the most appropriate goal based on user context.
        Considers competitive score, social score, and stress level.
        """
        # Calculate goal scores based on context
        goal_scores = {
            "compete_with_user": self._calculate_competitive_score(user_context),
            "engage_with_user": self._calculate_engagement_score(user_context),
            "pursue_personal_goals": self._calculate_personal_score(user_context)
        }

        # Apply weights to scores
        weighted_scores = {
            goal: score * self.goal_weights[goal]
            for goal, score in goal_scores.items()
        }

        # Select goal with highest weighted score
        return max(weighted_scores.items(), key=lambda x: x[1])[0]

    def _calculate_competitive_score(self, context: Dict[str, float]) -> float:
        """Calculate score for competitive goals based on user's competitive nature."""
        competitive_score = context.get("competitive_score", 0.5)
        energy_level = context.get("energy_level", 0.5)
        return (competitive_score + energy_level) / 2

    def _calculate_engagement_score(self, context: Dict[str, float]) -> float:
        """Calculate score for engagement goals based on user's social needs."""
        social_score = context.get("social_score", 0.5)
        # Higher score when social_score is low (user needs more engagement)
        return 1 - social_score

    def _calculate_personal_score(self, context: Dict[str, float]) -> float:
        """Calculate score for personal goals based on user's stress and energy levels."""
        stress_level = context.get("stress_level", 0.5)
        energy_level = context.get("energy_level", 0.5)
        # Higher score when stress is high or energy is low
        return (stress_level + (1 - energy_level)) / 2 