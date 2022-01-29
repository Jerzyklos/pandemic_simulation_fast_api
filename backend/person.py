from fast_api.backend.simulation_parameters import HealthState, X_DIM, Y_DIM
from random import random, randint


class Person:

    def __init__(self, parameters: dict):
        self.state = HealthState.HEALTHY
        self.x_pos = randint(0, X_DIM)
        self.y_pos = randint(0, Y_DIM)
        self.x_velocity = -0.5 + random()
        self.y_velocity = -0.5 + random()
        self.illness_duration = 0
        self.immunity_duration = 0
        self.quarantined = False
        # simulation parameters
        self.parameters = parameters

    def move(self):
        if self.state != HealthState.DEAD and (self.quarantined == False or self.parameters["quarantine"] == False):
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            # bouncing of the edges
            if self.x_pos >= X_DIM:
                self.x_pos = X_DIM
                self.x_velocity *= -1
            if self.x_pos <= 0:
                self.x_pos = 0
                self.x_velocity *= -1
            if self.y_pos >= Y_DIM:
                self.y_pos = Y_DIM
                self.y_velocity *= -1
            if self.y_pos <= 0:
                self.y_pos = 0
                self.y_velocity *= -1

    def simulate_illness(self):
        if self.state == HealthState.SYMPTOMATIC or self.state == HealthState.ASYMPTOMATIC:
            if self.illness_duration > self.parameters["min_duration_of_illness"]:
                random_value = random()
                if random_value <= self.parameters["recovery_probability"]:
                    self.state = HealthState.HEALTHY
                    self.illness_duration = 0
                    self.quarantined = False
                elif random_value < (self.parameters["recovery_probability"] + self.parameters["death_probability"]):
                    self.state = HealthState.DEAD
                    self.quarantined = False
            else:
                self.illness_duration += 1

    def infect(self):
        if random() < self.parameters["symptomatic_probability"]:
            self.state = HealthState.SYMPTOMATIC
            if random() < self.parameters["test_avaibility"]:
                self.quarantined = True
        else:
            self.state = HealthState.ASYMPTOMATIC

    def is_infecting(self):
        if (self.state == HealthState.ASYMPTOMATIC or self.state == HealthState.SYMPTOMATIC) and \
                (self.quarantined == False or self.parameters["quarantine"] == False):
            return True
        else:
            return False
