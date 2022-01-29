from enum import Enum


class HealthState(Enum):
    HEALTHY = "healthy"
    ASYMPTOMATIC = "asymptomatic"
    SYMPTOMATIC = "symptomatic"
    DEAD = "dead"


# Simulation parameters:
# probability of ill person at the beginning of the simulation
starting_illness_probability = 0.2
# probability of having symptomps when ill
# so asymptomatic probability = 1 - symptomatic_probability
symptomatic_probability = 0.5
# spreading probability when closer than spreading radius
spreading_probability = 0.2
spreading_radius = 2
# recovery or death probability after minimal duration of illness
min_duration_of_illness = 200
recovery_probability = 0.005
death_probability = 0.001
# how long after illness person is immune to contracting illness
min_immunity_duration = 200
max_immunity_duration = 600
# when quarantine is true, symptomatic persons don't move
# and don't spread illness, when tested
quarantine = True
# availibity of tests, 1 means full avaibility
test_avaibility = 0.9
# dimensions of board
X_DIM = 100
Y_DIM = 100
# for how long the simulation will go
simulation_steps = 10000


