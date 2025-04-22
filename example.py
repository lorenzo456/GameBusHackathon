from api import post_walk_activity
from npc_agent import NPC_Agent
import httpx
import asyncio
import requests
import json
import requests

def run_scenario(scenario_name: str, context: dict):
    """
    Run a single scenario with the given context.
    """
    # print(f"\n=== {scenario_name} ===")
    agent = NPC_Agent("FitnessBot")
    agent.act(context)
    agent.print_current_plan()

def main():
    # Scenario 1: Competitive scenario
    competitive_context = {
        "competitive_score": 0.8,
        "energy_level": 0.9,
        "social_score": 0.5,
        "stress_level": 0.3
    }
    run_scenario("Competitive Scenario", competitive_context)

    # # Scenario 2: Engagement scenario
    # engagement_context = {
    #     "competitive_score": 0.3,
    #     "energy_level": 0.6,
    #     "social_score": 0.2,  # Low social score triggers engagement
    #     "stress_level": 0.4
    # }
    # run_scenario("Engagement Scenario", engagement_context)

    # # Scenario 3: Personal goals scenario
    # personal_context = {
    #     "competitive_score": 0.4,
    #     "energy_level": 0.7,
    #     "social_score": 0.6,
    #     "stress_level": 0.8  # High stress triggers personal activities
    # }
    # run_scenario("Personal Goals Scenario", personal_context)


    # post_walk_activity(555) 

if __name__ == "__main__":
    main() 