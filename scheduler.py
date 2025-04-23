from typing import List
from activities import Activity
from tools import Toolset
import time

class ActivityScheduler:
    def __init__(self, tools: Toolset):
        self.tools = tools
        self.schedule: List[Activity] = []

    def add_activity(self, activity: Activity) -> None:
        """Add an activity to the schedule."""
        self.schedule.append(activity)

    def execute_schedule(self) -> None:
        """Execute all activities in the schedule in order with delays."""
        for activity in self.schedule:
            # Execute the activity
            if activity.steps:
                self._execute_steps_activity(activity)
            elif activity.name == "like_post":
                self._execute_like_post(activity)
            elif activity.name == "add_comment_on_post":
                self._execute_comment_post(activity)
            elif activity.name.startswith("Walk"):
                self._execute_steps_activity(activity)
            else:
                self._execute_personal_activity(activity)
            
            # Wait for the delay before next activity
            if activity.delay:
                print(f"Waiting {activity.delay} minutes before next activity...")
                # time.sleep(activity.delay * 60)  # Convert minutes to seconds
                time.sleep(activity.delay)  # seconds for testing purposes

    def _execute_steps_activity(self, activity: Activity) -> None:
        """Execute a steps-based activity."""
        print(f"Executing steps activity: {activity.name}")

    def _execute_like_post(self, activity: Activity) -> None:
        """Execute a like post activity."""
        print(f"Executing like post activity: {activity.name}")

    def _execute_comment_post(self, activity: Activity) -> None:
        """Execute a comment post activity."""
        print(f"Executing comment post activity: {activity.name}")

    def _execute_personal_activity(self, activity: Activity) -> None:
        """Execute a personal activity."""
        print(f"Executing personal activity: {activity.name}")

    def clear_schedule(self) -> None:
        """Clear the current schedule."""
        self.schedule = []

    def get_schedule(self) -> List[Activity]:
        """Get the current schedule."""
        return self.schedule 