from typing import Dict, Any, List

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
            "pursue_own_goals"
        ]
        
    def get_appropriate_goal(self, user_context: Dict[str, Any]) -> str:
        """
        Select the most appropriate goal based on user context.
        The goal is selected based on the highest ratio in the context.
        """
        # Get the ratios from context
        competitiveness = user_context.get("user_needs_competitiveness", 0.0)
        encouragement = user_context.get("user_needs_encouragement", 0.0)
        nothing = user_context.get("user_needs_nothing", 0.0)
        
        # Find the highest ratio
        max_ratio = max(competitiveness, encouragement, nothing)
        
        # Return the corresponding goal
        if max_ratio == competitiveness:
            return "compete_with_user"
        elif max_ratio == encouragement:
            return "engage_with_user"
        else:  # max_ratio == nothing
            return "pursue_own_goals" 