from fastapi import FastAPI
from enum import Enum
from typing import Optional, List
from fast_api.database_connection import MongoDB
from fast_api.simulation import run_simulation
from fast_api.base_models import SimulationParametersModel, SimulationStatistics
from fast_api.data_parser import DataParser
from pydantic import parse_obj_as


app = FastAPI()
mongoDB = MongoDB()
data_parser = DataParser()


@app.post("/simulation_parameters/")
async def set_new_parameters(simulation_parameters: SimulationParametersModel):
    data = data_parser.parse_parameters(simulation_parameters)
    mongoDB.set_new_parameters(data)
    return {"message": "Simulation paramaters set"}


@app.get("/simulation_parameters/", response_model=SimulationParametersModel)
async def get_parameters():
    parameters = mongoDB.return_parameters()[0]
    data = SimulationParametersModel.parse_obj(parameters)
    return data


@app.get("/")
async def root():
    return {"message": "Index"}


@app.get("/run/{n}")
async def run(n: int):
    # run_simulation(n)
    return {"n": str(n)}


# example: /statistics/?start=100
# example: /statistics/?start=100&stop=200
# get statistics for steps from start to stop, stop is voluntary
@app.get("/statistics/", response_model=List[SimulationStatistics])
async def statitics(start: int, stop: Optional[int] = None):
    if stop is None:
        stop = start
    stats = mongoDB.return_stats(start, stop)
    data = [SimulationStatistics.parse_obj(stat) for stat in stats]
    return data



# @app.get("/health/{state}")
# async def read_item(state: HealthState, start: Optional[int]=1, stop: Optional[int] = 4):
#     return {"state", data[start], data[stop]}
#     if state == HealthState.healthy:
#         return {"message": "patient healthy"}
#     elif state == HealthState.ill:
#         return {"message": "patient ill"}
#     elif state == HealthState.asymptomatic:
#         return {"message": "patient asymptomatic"}
#     elif state == HealthState.dead:
#         return {"message": "patient dead"}

# @app.get("/items/benek")
# async def read_item():
#     return {"message": "sekretny benek"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}