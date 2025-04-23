from typing import Dict, List
from tools import Toolset
from goals import GoalManager
from activities import Activity, select_activity, COMPETITIVE_ACTIVITIES, ENGAGEMENT_ACTIVITIES, PERSONAL_ACTIVITIES
from scheduler import ActivityScheduler
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def determine_activity_timing(activities: List[Activity], user_context: Dict[str, float]) -> List[Activity]:
    """
    Use an LLM to determine optimal delay between activities based on user context.
    
    Args:
        activities: List of activities to schedule
        user_context: User's current context (energy, stress, etc.)
        
    Returns:
        List of activities with delay information added
    """
    # Prepare the prompt for the LLM
    activity_list = [activity.name for activity in activities]
    prompt = f"""
    Given the following user context and activities, determine optimal delay between each activity.
    Consider the user's energy level, stress level, and activity intensity.
    
    User Context:
    - Energy Level: {user_context.get('energy_level', 0.5)}
    - Stress Level: {user_context.get('stress_level', 0.5)}
    - Competitive Score: {user_context.get('competitive_score', 0.5)}
    - Social Score: {user_context.get('social_score', 0.5)}
    
    Activities to schedule:
    {activity_list}
    
    For each activity, determine the delay (in minutes) before the next activity should start.
    Return ONLY a JSON object with activity names as keys and delay in minutes as values.
    Use the EXACT activity names from the list above.
    Example format:
    {{
        "Activity 1": 30,
        "Activity 2": 45,
        "Activity 3": 20
    }}
    """
    
    try:
        # Call the LLM using the new OpenAI API format
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fitness scheduling assistant. Always respond with valid JSON using the exact activity names provided."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Parse the LLM response
        schedule = response.choices[0].message.content
        import json
        timing_data = json.loads(schedule)
        
        # Debug print to see what we're working with
        # print("Activity names in timing data:", list(timing_data.keys()))
        # print("Our activity names:", [activity.name for activity in activities])
        
        # Update activities with delay information
        for activity in activities:
            # Try exact match first
            if activity.name in timing_data:
                activity.delay = timing_data[activity.name]
            else:
                # Try case-insensitive match
                activity_name_lower = activity.name.lower()
                matching_key = next((key for key in timing_data.keys() if key.lower() == activity_name_lower), None)
                if matching_key:
                    activity.delay = timing_data[matching_key]
                else:
                    print(f"Warning: No delay found for activity '{activity.name}'")
                    activity.delay = 30  # Default delay if not found
        
        return activities
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response: {schedule}")
        # Fallback to default delay if JSON parsing fails
        for activity in activities:
            activity.delay = 30
        return activities
    except Exception as e:
        print(f"Error determining activity timing: {e}")
        # Fallback to default delay if LLM fails
        for activity in activities:
            activity.delay = 30  # Default 30-minute delay
        return activities
    
def create_message_for_latest_player_walking_activity(user_context: Dict[str, float]) -> str:
    """
    Generate an encouraging message for the player's walking activity based on their context.
    
    Args:
        user_context: Dictionary containing user's current context (energy, stress, etc.)
        
    Returns:
        str: An encouraging message tailored to the user's context
    """
    prompt = f"""
    Generate an encouraging message for a player's walking activity progress.
    Consider the following user context:
    - Energy Level: {user_context.get('energy_level', 0.5)}
    - Stress Level: {user_context.get('stress_level', 0.5)}
    - Competitive Score: {user_context.get('competitive_score', 0.5)}
    - Social Score: {user_context.get('social_score', 0.5)}
    
    The message should be:
    1. Positive and encouraging
    2. Tailored to the user's current energy and stress levels
    3. Include a motivational element
    4. Be concise (1-2 sentences)
    5. Feel personal and genuine
    6. Less robotic, more like a humanlike - be more like a friend
    7. Be short and to the point - based on real life short social media messages
    
    Return ONLY the message text, no additional formatting or explanation.
    """
    
    try:
        # Call the LLM using the new OpenAI API format
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive fitness coach. Generate encouraging messages that are personal and motivating."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating message: {e}")
        # Fallback to a generic encouraging message
        return "Great job on your walking activity! Every step counts towards your health goals. Keep it up!"

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
            if hasattr(activity, 'delay'):
                plan_str += f"\n   Delay before next: {activity.delay}min"
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

    def add_plan_to_scheduler(self, user_context: Dict[str, float]) -> None:
        """Add all activities from the current plan to the scheduler with optimal timing."""
        # Determine optimal timing for activities
        scheduled_activities = determine_activity_timing(self.current_plan, user_context)
        
        #strip the name from walking activities using the check_activity_name_includes_steps function
        for activity in scheduled_activities:
            if activity.name.startswith("Walk"):
                activity.name = check_activity_name_includes_steps(activity.name)
        
        # Add activities to scheduler
        for activity in scheduled_activities:
            self.scheduler.add_activity(activity)



