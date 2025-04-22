from typing import List
from activities import Activity
from tools import Toolset

class ActivityScheduler:
    def __init__(self, tools: Toolset):
        self.tools = tools
        self.schedule: List[Activity] = []

    def add_activity(self, activity: Activity) -> None:
        """Add an activity to the schedule."""
        self.schedule.append(activity)

    def execute_schedule(self) -> None:
        """Execute all activities in the schedule in order."""
        for activity in self.schedule:
            if activity.steps:
                self._execute_steps_activity(activity)
            elif activity.name == "like_post":
                self._execute_like_post(activity)
            elif activity.name == "add_comment_on_post":
                self._execute_comment_post(activity)


    def _execute_steps_activity(self, activity: Activity) -> None:
        """Execute a steps-based activity."""
        # TODO: Implement steps activity execution
        pass

    def _execute_like_post(self, activity: Activity) -> None:
        """Execute a like post activity."""
        # TODO: Implement like post execution
        pass

    def _execute_comment_post(self, activity: Activity) -> None:
        """Execute a comment post activity."""
        # TODO: Implement comment post execution
        pass

    def _execute_personal_activity(self, activity: Activity) -> None:
        """Execute a personal activity."""
        # TODO: Implement personal activity execution
        pass

    def clear_schedule(self) -> None:
        """Clear the current schedule."""
        self.schedule = []

    def get_schedule(self) -> List[Activity]:
        """Get the current schedule."""
        return self.schedule 