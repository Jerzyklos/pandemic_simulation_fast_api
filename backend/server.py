from fastapi import FastAPI
from typing import List
from fast_api.backend.database_connection import MongoDB
from fast_api.backend.simulation import run_simulation
from fast_api.backend.base_models import *
from fast_api.backend.data_parser import DataParser


app = FastAPI()
mongoDB = MongoDB()


@app.post("/simulation_parameters/")
async def set_new_parameters(simulation_parameters: SimulationParametersModel):
    data_parser = DataParser()
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


@app.post("/run/{n}")
async def run(n: int):
    run_simulation(n) # TODO it freezes the server until it's done
    return {"Info": "Simulation done"}


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


# example: /persons/?step=100
# get persons position and state for step
@app.get("/persons/", response_model=List[PersonsPositionAndState])
async def persons(step: int):
    persons = mongoDB.return_persons(step)[0]["persons"]
    data = [PersonsPositionAndState.parse_obj(person) for person in persons]
    return data
