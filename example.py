from api import get_latest_player_walking_activity, post_message_on_latest_player_walking_activity, post_walk_activity
from npc_agent import NPC_Agent
import httpx
import asyncio
import requests
import json
import requests
from typing import Dict

from scheduler import ActivityScheduler

def run_scenario(scenario_name: str, context: dict):
    """
    Run a single scenario with the given context.
    """
    # print(f"\n=== {scenario_name} ===")
    agent = NPC_Agent("Standard NPC")
    agent.act(context)
    agent.add_plan_to_scheduler(context)
    # print(agent.scheduler.get_schedule())
    agent.scheduler.execute_schedule(context)

def analyze_player_context() -> Dict[str, float]:
    """
    Analyze player context from activity logs.
    Determines whether to use competitive or engagement scenario based on player behavior.
    
    Returns:
        Dict[str, float]: Context for either competitive or engagement scenario
    """
    # Load activity logs
    with open('activity_logs.json', 'r') as f:
        activity_logs = json.load(f)
    
    if not activity_logs.get("activities"):
        # Default to engagement scenario if no activities
        return {
            "competitive_score": 0.3,
            "energy_level": 0.6,
            "social_score": 0.2,
            "stress_level": 0.4
        }
    
    activities = activity_logs["activities"]
    
    # Calculate metrics
    total_steps = sum(activity["steps"] for activity in activities)
    avg_steps = total_steps / len(activities)
    total_comments = sum(len(activity["comments"]) for activity in activities)
    
    # Calculate trend (last activity steps vs first activity steps)
    if len(activities) >= 2:
        first_steps = activities[0]["steps"]
        last_steps = activities[-1]["steps"]
        progress = (last_steps - first_steps) / first_steps
    else:
        progress = 0
    
    # Determine if player is competitive or needs engagement
    is_competitive = (
        avg_steps > 7000 or  # High average steps
        progress > 0.3 or    # Significant progress
        total_comments < 1   # Low social interaction
    )
    
    if is_competitive:
        print("Player context is competitive")
        return {
            "competitive_score": 0.8,
            "energy_level": 0.9,
            "social_score": 0.5,
            "stress_level": 0.3
        }
    else:
        print("Player context is engagement")
        return {
            "competitive_score": 0.3,
            "energy_level": 0.6,
            "social_score": 0.2,
            "stress_level": 0.4
        }

def main():
    # Get player context from activity logs
    player_context = analyze_player_context()
    
    # Run scenario with determined context
    run_scenario("Player Context Scenario", player_context)
    
    # # Scenario 1: Competitive scenario
    # competitive_context = {
    #     "competitive_score": 0.8,
    #     "energy_level": 0.9,
    #     "social_score": 0.5,
    #     "stress_level": 0.3
    # }
    # run_scenario("Competitive Scenario", competitive_context)

    # # Scenario 2: Engagement scenario
    # engagement_context = {
    #     "competitive_score": 0.3,
    #     "energy_level": 0.6,
    #     "social_score": 0.2,  # Low social score triggers engagement
    #     "stress_level": 0.4
    # }
    # run_scenario("Engagement Scenario", engagement_context)

if __name__ == "__main__":
    main() 