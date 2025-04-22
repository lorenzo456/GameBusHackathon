from npc_agent import NPC_Agent
import httpx
import asyncio
import requests
import json
import requests

def run_scenario(scenario_name: str, user_context: dict):
    print("User Context:", user_context)
    
    agent = NPC_Agent("user123")
    agent.set_goal(user_context)
    print(f"Selected Goal: {agent.current_goal}")
    
    agent.act(user_context)

# Scenario 1: User needs competitiveness
competitive_context = {
    "user_needs_competitiveness": 0.8,  # High need for competition
    "user_needs_encouragement": 0.1,    # Low need for encouragement
    "user_needs_nothing": 0.1           # Low need for nothing
}

# Scenario 2: User needs encouragement
engagement_context = {
    "user_needs_encouragement": 0.8,    # High need for encouragement
    "user_needs_competitiveness": 0.1,  # Low need for competition
    "user_needs_nothing": 0.1           # Low need for nothing
}

# Scenario 3: User needs nothing
personal_context = {
    "user_needs_nothing": 0.8,          # High need for nothing
    "user_needs_encouragement": 0.1,    # Low need for encouragement
    "user_needs_competitiveness": 0.1   # Low need for competition
}

def post_activity():
    url = "https://api.healthyw8.gamebus.eu/v2/activities?dryrun=false&fields=personalPoints"

    payload = {}
    files=[
        ('activity', ('activity.json', open('activity.json', 'rb'), 'application/json'))
    ]
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZ2FtZWJ1c19hcGkiXSwidXNlcl9uYW1lIjoibC5qLmphbWVzK2FnZW50czFAdHVlLm5sIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIiwidHJ1c3QiLCJkZWxldGU6YWN0aXZpdHkiXSwiZXhwIjoxODIzMDg5ODU1LCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6IlJ1ZzFpd201RGEzY19NLUtIVF84aFZMQTJiWSIsImNsaWVudF9pZCI6ImdhbWVidXNfc3R1ZGlvX2FwcCJ9.mjkXdOCfhxHFtPGrLfFvivU3SvKGzhDnKY8QHKpwIK9SHbzbKgQLIEMdvzprU6bAeTl9IhSQmXUCYlkyKtXVIGqIfGF7yZ1pFu-MNAoePRDPt1rjr6NMoEgKCAvCGTNK7Of5cM0MJS2UWs3fr9kMRXlFeKu8XtipG5kha9kwqsflh_L1Flw_4PZc73EfK0igCJ9PNHQBNFLIG1SwVgS0Qsw0S4V9GMQtOWRq1Fzt7IUlAcKTHVpMPnw6lNVvFX3PlYKCxm3GNjw0K-YI7iQSNJYZ1_BYPuP3EJwt13FyOi8XLH_3OqX9HrzRS8hWhXJbFFTih5nUieciHjtaaJthsw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def main():
    # Run all scenarios
    run_scenario("Competitive Athlete Scenario", competitive_context)
    # run_scenario("Social Engagement Scenario", engagement_context)
    # run_scenario("Personal Development Scenario", personal_context)
    
    # post_activity() 

if __name__ == "__main__":
    main() 