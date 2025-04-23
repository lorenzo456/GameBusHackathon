from api import get_latest_player_walking_activity, post_message_on_latest_player_walking_activity, post_walk_activity
from npc_agent import NPC_Agent
import httpx
import asyncio
import requests
import json
import requests
from typing import Dict
import openai
import random

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
    Analyze player context from activity logs using an LLM.
    Determines whether to use competitive or engagement scenario based on player behavior.
    
    Returns:
        Dict[str, float]: Context for either competitive or engagement scenario
    """
    # Load activity logs
    with open('activity_logs_llm.json', 'r') as f:
        activity_logs = json.load(f)
    
    if not activity_logs.get("activities"):
        # Default to engagement scenario if no activities
        return {
            "competitive_score": 0.3,
            "energy_level": 0.6,
            "social_score": 0.2,
            "stress_level": 0.4
        }
    
    # Prepare the prompt for the LLM
    activities_str = json.dumps(activity_logs["activities"], indent=2)
    prompt = f"""
    Analyze these activity logs and determine if the player's behavior is competitive or needs social engagement.
    Consider factors like:
    - Activity types (walking vs social activities)
    - Step counts and progress
    - Social interaction (comments)
    - Activity frequency and consistency
    
    Activity Logs:
    {activities_str}
    
    Return a JSON object with:
    1. is_competitive: boolean (true if competitive, false if needs engagement)
    2. reasoning: string (brief explanation of your analysis)
    
    Example format:
    {{
        "is_competitive": true,
        "reasoning": "Player shows high step counts and consistent activity patterns"
    }}
    """
    
    try:
        # Call the LLM using the new OpenAI API format
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fitness behavior analyst. Analyze activity logs to determine if a player is competitive or needs social engagement."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Parse the LLM response
        analysis = json.loads(response.choices[0].message.content)
        # print(f"Analysis: {analysis['reasoning']}")
        
        # Return appropriate context based on analysis
        if analysis["is_competitive"]:
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
        
    except Exception as e:
        print(f"Error analyzing player context: {e}")
        # Default to engagement scenario if analysis fails
        return {
            "competitive_score": 0.3,
            "energy_level": 0.6,
            "social_score": 0.2,
            "stress_level": 0.4
        }
    
def randomly_generate_activity_logs():
    is_competitive = random.choice([True, False])  # or set manually

    if is_competitive:
        prompt = """
    Generate a realistic JSON file containing 1 to 5 walking activity logs for a fitness app.

    Each activity should have:
    - A unique ID
    - Type: "walking"
    - Steps: between 1000 and 15000
    - Timestamp: within the last 7 days or 30 days ago
    - Duration: between 15 and 120 minutes
    - Calories: proportional to steps
    - Distance: roughly 0.7km per 1000 steps
    - Player info: id: 921, name: "John Doe"
    - Points: between 10 and 100
    - 0-2 comments per activity

    Return ONLY the JSON object, no additional text or explanation.

    The JSON should follow this exact structure:
    {
        "activities": [
            {
                "id": number,
                "type": "walking",
                "steps": number,
                "timestamp": "ISO8601",
                "duration": number,
                "calories": number,
                "distance": number,
                "player": {
                    "id": 921,
                    "name": "John Doe"
                },
                "points": number,
                "comments": [
                    {
                        "id": number,
                        "player_id": number,
                        "message": string,
                        "timestamp": "ISO8601"
                    }
                ]
            }
        ]
    }
    """
    else:
        prompt = """
    Generate a realistic JSON file containing 1 to 5 non-physical social activity logs for a fitness app.

    Each activity should have:
    - A unique ID
    - Type: e.g., "reading", "book club", "chatting", etc.
    - Timestamp: within the last 7 days or 30 days ago
    - Duration: between 15 and 120 minutes
    - Calories: proportional to duration (can be low)
    - Player info: id: 921, name: "John Doe"
    - Points: between 10 and 100
    - 0-2 comments per activity

    Return ONLY the JSON object, no additional text or explanation.

    The JSON should follow this exact structure:
    {
        "activities": [
            {
                "id": number,
                "type": string,
                "timestamp": "ISO8601",
                "duration": number,
                "calories": number,
                "player": {
                    "id": 921,
                    "name": "John Doe"
                },
                "points": number,
                "comments": [
                    {
                        "id": number,
                        "player_id": number,
                        "message": string,
                        "timestamp": "ISO8601"
                    }
                ]
            }
        ]
    }
    """

    
    try:
        # Call the LLM using the new OpenAI API format
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data generator for a fitness app. Generate realistic activity logs in JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Get the generated JSON and parse it to ensure it's valid
        activity_logs = json.loads(response.choices[0].message.content)
        
        # Save to file with proper formatting
        with open('activity_logs_llm.json', 'w', encoding='utf-8') as f:
            json.dump(activity_logs, f, indent=4, ensure_ascii=False)
            
        print("Successfully generated new activity logs in activity_logs_llm.json")
        
    except Exception as e:
        print(f"Error generating activity logs: {e}")
        # Fallback to a simple activity log
        fallback_logs = {
            "activities": [
                {
                    "id": 12345,
                    "type": "walking",
                    "steps": 5000,
                    "timestamp": "2024-03-15T10:30:00Z",
                    "duration": 45,
                    "calories": 250,
                    "distance": 3.5,
                    "player": {
                        "id": 921,
                        "name": "John Doe"
                    },
                    "points": 50,
                    "comments": []
                }
            ]
        }
        with open('activity_logs_llm.json', 'w', encoding='utf-8') as f:
            json.dump(fallback_logs, f, indent=4, ensure_ascii=False)
        print("Generated fallback activity logs in activity_logs_llm.json")


def main():
    # Generate new random activity logs
    randomly_generate_activity_logs()
    
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