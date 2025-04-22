from npc_agent import NPC_Agent

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

def main():
    """Run all NPC agent scenarios."""
    print("Starting NPC Agent Scenarios...")
    print("="*50)
    
    # Run all scenarios
    run_scenario("Competitive Athlete Scenario", competitive_context)
    run_scenario("Social Engagement Scenario", engagement_context)
    run_scenario("Personal Development Scenario", personal_context)
    
    print("\nAll scenarios completed!")

if __name__ == "__main__":
    main() 