import json
from typing import Dict
import openai
import requests

def post_walk_activity(steps: int):
    url = "https://api.healthyw8.gamebus.eu/v2/activities?dryrun=false&fields=personalPoints"
    
    with open('walk_activity.json', 'r') as file:
        data = json.load(file)
        data['propertyInstances'] = [{"property":20,"value":steps}]
        
    with open('walk_activity.json', 'w') as file:
        json.dump(data, file)

    payload = {}
    files=[
        ('activity', ('walk_activity.json', open('walk_activity.json', 'rb'), 'application/json'))
    ]
    #update value in walk_activity.json

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZ2FtZWJ1c19hcGkiXSwidXNlcl9uYW1lIjoibC5qLmphbWVzK2FnZW50czFAdHVlLm5sIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIiwidHJ1c3QiLCJkZWxldGU6YWN0aXZpdHkiXSwiZXhwIjoxODIzMDg5ODU1LCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6IlJ1ZzFpd201RGEzY19NLUtIVF84aFZMQTJiWSIsImNsaWVudF9pZCI6ImdhbWVidXNfc3R1ZGlvX2FwcCJ9.mjkXdOCfhxHFtPGrLfFvivU3SvKGzhDnKY8QHKpwIK9SHbzbKgQLIEMdvzprU6bAeTl9IhSQmXUCYlkyKtXVIGqIfGF7yZ1pFu-MNAoePRDPt1rjr6NMoEgKCAvCGTNK7Of5cM0MJS2UWs3fr9kMRXlFeKu8XtipG5kha9kwqsflh_L1Flw_4PZc73EfK0igCJ9PNHQBNFLIG1SwVgS0Qsw0S4V9GMQtOWRq1Fzt7IUlAcKTHVpMPnw6lNVvFX3PlYKCxm3GNjw0K-YI7iQSNJYZ1_BYPuP3EJwt13FyOi8XLH_3OqX9HrzRS8hWhXJbFFTih5nUieciHjtaaJthsw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def get_latest_player_walking_activity():
    url = "https://api.healthyw8.gamebus.eu/v2/players/14/activities?gds=walk&sort=-date&limit=1"

    payload = {}
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZ2FtZWJ1c19hcGkiXSwidXNlcl9uYW1lIjoibC5qLmphbWVzQHR1ZS5ubCIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSIsInRydXN0IiwiZGVsZXRlOmFjdGl2aXR5Il0sImV4cCI6MTgyMzA4OTY2NywiYXV0aG9yaXRpZXMiOlsiQURNSU4iLCJDQU1QQUlHTl9PUkdBTklaRVIiLCJERVYiLCJVU0VSIl0sImp0aSI6IlBwUTZlb2d4dVBkWGxRSEpGcjkzMlYtblJOUSIsImNsaWVudF9pZCI6ImdhbWVidXNfc3R1ZGlvX2FwcCJ9.mhUGYNLgAEt_jVWl8rZEbxddPfJvKbaRjAobCeOZOTmnhAf853McX-KFmssD4ll4JihFghXnvNBp3YmzXW1GcA2XpredaX-5h_uOWfvmT6QR6Pd1g0XW1E2cVNtbnFGZIOuV0aXj8AyelujSXIAYThIs5eqnrrYkC_cEY70CzauBU0pxEQZGH6wbWos3tlOTERxgDkxNrmHiam4Cf9yf4hziF5T6_x4PmsS7KfwyGN7L1_MUUNfkbhT40F3-BbJtzTs9Dt1q93YfRPer_EnY8OI6-vK1sGc9SQFDaP3dSl2zXteN4_IAEUUM1YvwAG2HqrdjtAappVBXcBMtfeUZ1Q'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    #get the id of the activity
    activity_id = response_json[0]['id']

    return activity_id


def post_message_on_latest_player_walking_activity(message):
    activity_id = get_latest_player_walking_activity()

    url = f"https://api.healthyw8.gamebus.eu/v2/activities/{activity_id}/messages"

    payload = json.dumps({
    "text": message
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZ2FtZWJ1c19hcGkiXSwidXNlcl9uYW1lIjoibC5qLmphbWVzK2FnZW50czFAdHVlLm5sIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIiwidHJ1c3QiLCJkZWxldGU6YWN0aXZpdHkiXSwiZXhwIjoxODIzMDg5ODU1LCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6IlJ1ZzFpd201RGEzY19NLUtIVF84aFZMQTJiWSIsImNsaWVudF9pZCI6ImdhbWVidXNfc3R1ZGlvX2FwcCJ9.mjkXdOCfhxHFtPGrLfFvivU3SvKGzhDnKY8QHKpwIK9SHbzbKgQLIEMdvzprU6bAeTl9IhSQmXUCYlkyKtXVIGqIfGF7yZ1pFu-MNAoePRDPt1rjr6NMoEgKCAvCGTNK7Of5cM0MJS2UWs3fr9kMRXlFeKu8XtipG5kha9kwqsflh_L1Flw_4PZc73EfK0igCJ9PNHQBNFLIG1SwVgS0Qsw0S4V9GMQtOWRq1Fzt7IUlAcKTHVpMPnw6lNVvFX3PlYKCxm3GNjw0K-YI7iQSNJYZ1_BYPuP3EJwt13FyOi8XLH_3OqX9HrzRS8hWhXJbFFTih5nUieciHjtaaJthsw'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def post_message(user_context: Dict[str, float]):
    message = create_message_for_latest_player_walking_activity(user_context)
    post_message_on_latest_player_walking_activity(message)


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
