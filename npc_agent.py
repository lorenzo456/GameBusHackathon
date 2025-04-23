from typing import Dict, List
from tools import Toolset
from goals import GoalManager
from activities import Activity, select_activity, COMPETITIVE_ACTIVITIES, ENGAGEMENT_ACTIVITIES, PERSONAL_ACTIVITIES
from scheduler import ActivityScheduler

def check_activity_name_includes_steps(activity_name: str) -> int:
    """
    Check if the activity name includes steps and extract the step count.
    
    Args:
        activity_name (str): The name of the activity to check
        
    Returns:
        int: The number of steps found in the activity name, or None if no steps found
        
    Examples:
        >>> check_activity_name_includes_steps("Walk 5000 steps")
        5000
        >>> check_activity_name_includes_steps("Run 10k steps")
        10000
        >>> check_activity_name_includes_steps("Yoga session")
        None
    """
    # Convert to lowercase for case-insensitive matching
    name = activity_name.lower()
    
    # Common step-related keywords
    step_keywords = ["steps", "step", "walk", "run", "jog"]
    
    # Check if the activity name contains any step-related keywords
    if not any(keyword in name for keyword in step_keywords):
        return None
        
    # Extract all numbers from the string
    import re
    numbers = re.findall(r'\d+', activity_name)
    
    # If no numbers found, return None
    if not numbers:
        return None
        
    # Convert the first number found to integer
    step_count = int(numbers[0])
    
        
    return step_count

class NPC_Agent:
    def __init__(self, name: str):
        self.name = name
        self.tools = Toolset()
        self.goal_manager = GoalManager()
        self.current_goal = None
        self.current_activities = []
        self.current_plan = []
        self.scheduler = ActivityScheduler(self.tools)

    def set_goal(self, user_context: Dict[str, float]) -> None:
        """
        Set the current goal based on user context.
        """
        self.current_goal = self.goal_manager.select_goal(user_context)
        # print(f"{self.name} has set a new goal: {self.current_goal}")

    def add_to_plan(self, activity: Activity) -> None:
        """
        Add an activity to the current plan.
        """
        # Check if the activity name includes steps
        steps = check_activity_name_includes_steps(activity.name)
        if steps is not None:
            # Create a new activity with the extracted steps
            activity = Activity(activity.name, activity.intensity, steps)
        
        self.current_plan.append(activity)
        # print(f"Added to plan: {activity.name} (Intensity: {activity.intensity:.2f})")

    def get_current_plan(self) -> str:
        """Return a formatted string of the current plan."""
        if not self.current_plan:
            return f"{self.name} has no activities in the current plan."

        plan_str = f"\nCurrent Plan for {self.name}:"
        total_intensity = sum(activity.intensity for activity in self.current_plan)
        plan_str += f"\nTotal planned intensity: {total_intensity:.2f}"
        plan_str += "\nActivities:"
        for i, activity in enumerate(self.current_plan, 1):
            if activity.steps:
                plan_str += f"\n{i}. {activity.name} (Intensity: {activity.intensity:.2f}, Steps: {activity.steps})"
            else:
                plan_str += f"\n{i}. {activity.name} (Intensity: {activity.intensity:.2f})"
        return plan_str

    def act(self, user_context: Dict[str, float]) -> None:
        """
        Perform actions based on the current goal and user context.
        """
        if not self.current_goal:
            self.set_goal(user_context)

        # Select appropriate activities based on the goal
        if self.current_goal == "compete_with_user":
            self.current_activities = select_activity(COMPETITIVE_ACTIVITIES, user_context, "compete_with_user")
            for activity in self.current_activities:
                self.add_to_plan(activity)
            self._perform_competitive_activities()
        
        elif self.current_goal == "engage_with_user":
            self.current_activities = select_activity(ENGAGEMENT_ACTIVITIES, user_context, "engage_with_user")
            for activity in self.current_activities:
                self.add_to_plan(activity)
            self._perform_engagement_activities()
        
        elif self.current_goal == "pursue_personal_goals":
            self.current_activities = select_activity(PERSONAL_ACTIVITIES, user_context, "pursue_personal_goals")
            for activity in self.current_activities:
                self.add_to_plan(activity)
            self._perform_personal_activities()

    def _perform_competitive_activities(self) -> None:
        """
        Perform a sequence of competitive activities.
        """
        if not self.current_activities:
            print(f"{self.name} couldn't find suitable competitive activities.")
            return

        total_steps = sum(activity.steps for activity in self.current_activities if activity.steps)


    def _perform_engagement_activities(self) -> None:
        """
        Perform a sequence of engagement activities.
        """
        if not self.current_activities:
            print(f"{self.name} couldn't find suitable engagement activities.")
            return

        print(f"{self.name} is performing engagement activities:")
        for activity in self.current_activities:
            if activity.name == "like_post":
                self.tools.like_post()
            elif activity.name == "add_comment_on_post":
                self.tools.add_comment_on_post()
            print(f"- {activity.name} (Intensity: {activity.intensity:.2f})")

    def _perform_personal_activities(self) -> None:
        """
        Perform a sequence of personal activities.
        """
        if not self.current_activities:
            print(f"{self.name} couldn't find suitable personal activities.")
            return

        print(f"{self.name} is performing personal activities:")
        for activity in self.current_activities:
            print(f"- {activity.name} (Intensity: {activity.intensity:.2f})")

    def add_plan_to_scheduler(self) -> None:
        """Add all activities from the current plan to the scheduler."""
        for activity in self.current_plan:
            self.scheduler.add_activity(activity) 