from fastapi import FastAPI
from enum import Enum
from typing import Optional

class HealthState(str, Enum):
    healthy = "healthy"
    ill = "ill"
    asymptomatic = "asymptomatic"
    dead = "dead"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Beniz"}

data = [HealthState.healthy, HealthState.ill, HealthState.asymptomatic, HealthState.healthy,
        HealthState.healthy, HealthState.ill, HealthState.asymptomatic, HealthState.healthy]

@app.get("/health/{state}")
async def read_item(state: HealthState, start: Optional[int]=1, stop: Optional[int] = 4):
    return {"state", data[start], data[stop]}
    if state == HealthState.healthy:
        return {"message": "patient healthy"}
    elif state == HealthState.ill:
        return {"message": "patient ill"}
    elif state == HealthState.asymptomatic:
        return {"message": "patient asymptomatic"}
    elif state == HealthState.dead:
        return {"message": "patient dead"}

@app.get("/items/benek")
async def read_item():
    return {"message": "sekretny benek"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}