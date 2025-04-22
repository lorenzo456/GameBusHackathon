# GameBusHackathon

A gamified health app featuring an intelligent NPC agent system.

## Project Structure

- `npc_agent.py`: Main NPC agent class that handles decision making and action execution
- `tools.py`: Contains the Toolset class with available actions (send_message, like_post, schedule_activity)
- `goals.py`: Contains the GoalManager class and predefined goals
- `example.py`: Example usage of the NPC agent system

## Features

- Intelligent NPC agents that can interact with users
- Goal-based decision making
- Modular tool system for various actions
- Context-aware behavior

## Usage

Run the example script to see the NPC agent in action:

```bash
python example.py
```

## Future Improvements

- Integrate with an LLM for more sophisticated decision making
- Add more tools and actions
- Implement real API connections for tools
- Add more complex goal selection logic
- Implement user feedback and learning