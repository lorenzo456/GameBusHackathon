from typing import List, Dict, Any
from tools import Toolset
from goals import GoalManager
from activities import (
    COMPETITIVE_ACTIVITIES,
    ENGAGEMENT_ACTIVITIES,
    PERSONAL_ACTIVITIES,
    select_activity
)

class NPC_Agent:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.current_goal = None
        self.tools = Toolset()
        self.goal_manager = GoalManager()
        
    def set_goal(self, user_context: Dict[str, Any]) -> None:
        """Set the current goal based on user context."""
        self.current_goal = self.goal_manager.get_appropriate_goal(user_context)
        
    def act(self, user_context: Dict[str, Any]) -> None:
        """
        Determine and execute the next best action based on user context.
        
        Args:
            user_context: Dictionary containing user's current state and history
        """
        if not self.current_goal:
            self.set_goal(user_context)
            
        # Convert context to float values for activity selection
        context_scores = {k: float(v) for k, v in user_context.items() if isinstance(v, (int, float))}
            
        if self.current_goal == "compete_with_user":
            activity = select_activity(COMPETITIVE_ACTIVITIES, context_scores)
            self.tools.perform_activity(activity.name, activity.duration)
        elif self.current_goal == "engage_with_user":
            activity = select_activity(ENGAGEMENT_ACTIVITIES, context_scores)
            if activity.name == "like_post":
                self.tools.like_post("Great job on your activity! Keep it up!")
            else:  # add_comment_on_post
                self.tools.add_comment_on_post("I noticed your progress - you're doing amazing! Keep going!")
        else:  # pursue_own_goals
            activity = select_activity(PERSONAL_ACTIVITIES, context_scores)
            self.tools.perform_activity(activity.name, activity.duration) 