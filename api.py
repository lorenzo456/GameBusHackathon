from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import httpx
import os
from dotenv import load_dotenv

app = FastAPI()

class PropertyInstance(BaseModel):
    property: int
    value: int

class ActivityRequest(BaseModel):
    gameDescriptor: int
    dataProviderName: str
    propertyInstances: List[PropertyInstance]
    players: List[int]

load_dotenv()
GAMEBUS_API_URL = "https://api.healthyw8.gamebus.eu/v2/activities"
GAMEBUS_BEARER_TOKEN = os.getenv("GAMEBUS_BEARER_TOKEN")

@app.post("/post_activity")
async def post_activity(activity: ActivityRequest):
    if not GAMEBUS_BEARER_TOKEN:
        raise HTTPException(status_code=500, detail="GameBus bearer token not configured")
    
    headers = {
        "Authorization": f"Bearer {GAMEBUS_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    params = {
        "dryrun": "false",
        "fields": "personalPoints"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GAMEBUS_API_URL,
                headers=headers,
                params=params,
                json=activity.dict()
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code if hasattr(e, 'response') else 500,
            detail=f"GameBus API error: {str(e)}"
        )

