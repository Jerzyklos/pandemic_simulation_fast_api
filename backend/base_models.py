from pydantic import BaseModel
from typing import Optional

# Model used for setting new simulation parameters
class SimulationParametersModel(BaseModel):
    starting_illness_probability: float
    symptomatic_probability: float
    spreading_probability: float
    spreading_radius: float
    min_duration_of_illness: int
    recovery_probability: float
    death_probability: float
    min_immunity_duration: int
    max_immunity_duration: int
    quarantine: bool
    test_availability: float
    simulation_steps: int


# Model used for returning simulation statistics
class SimulationStatistics(BaseModel):
    step: int
    healthy: int
    symptomatic: int
    asymptomatic: int


# Model used for returning persons positions and states
class PersonsPositionAndState(BaseModel):
    x: int
    y: int
    state: str

