from pydantic import BaseModel


# Request body used for setting new simulation parameters
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
    test_avaibility: float
    simulation_steps: int