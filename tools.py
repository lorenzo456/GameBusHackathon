class Toolset:
    def add_comment_on_post(self, message: str) -> None:
        """Add a comment to a user's post."""
        print(f"[COMMENT] {message}")
        
    def like_post(self, message: str) -> None:
        """Like a user's post with a supportive message."""
        print(f"[LIKE] {message}")
        
    def perform_activity(self, activity_type: str, duration: int) -> None:
        """
        Perform an activity as the NPC agent.
        
        Args:
            activity_type: Type of activity (e.g., 'workout', 'meditation', 'walk')
            duration: Duration of the activity in minutes
        """
        print(f"[ACTIVITY] NPC is performing {activity_type} for {duration} minutes") 