import pygame
from enum import Enum
from random import random, randint
from typing import List, Dict, Tuple
from time import sleep
from math import sqrt
# all the simulation parameters
from simulation_parameters import *


class HealthState(Enum):
    HEALTHY = "healthy"
    ASYMPTOMATIC = "asymptomatic"
    SYMPTOMATIC = "symptomatic"
    DEAD = "dead"


def health_state_colors() -> Dict[HealthState, pygame.Color]:
    colors = {}
    colors[HealthState.HEALTHY] = pygame.Color("green")
    colors[HealthState.SYMPTOMATIC] = pygame.Color("red")
    colors[HealthState.ASYMPTOMATIC] = pygame.Color("yellow")
    colors[HealthState.DEAD] = pygame.Color("black")
    return colors


class Person:

    def __init__(self):
        self.state = HealthState.HEALTHY
        self.x_pos = randint(0, X_DIM)
        self.y_pos = randint(0, Y_DIM)
        self.x_velocity = -0.5 + random()
        self.y_velocity = -0.5 + random()
        self.illness_duration = 0
        self.immunity_duration = 0
        self.quarantined = False

    def move(self):
        if self.state != HealthState.DEAD and (self.quarantined == False or quarantine == False):
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
            if self.illness_duration > min_duration_of_illness:
                random_value = random()
                if random_value <= recovery_probability:
                    self.state = HealthState.HEALTHY
                    self.illness_duration = 0
                    self.quarantined = False
                elif random_value < (recovery_probability + death_probability):
                    self.state = HealthState.DEAD
                    self.quarantined = False
            else:
                self.illness_duration += 1

    def infect(self):
        if random() < symptomatic_probability:
            self.state = HealthState.SYMPTOMATIC
            if random() < test_avaibility:
                self.quarantined = True
        else:
            self.state = HealthState.ASYMPTOMATIC

    def is_infecting(self):
        if (self.state == HealthState.ASYMPTOMATIC or self.state == HealthState.SYMPTOMATIC) and \
                (self.quarantined == False or quarantine == False):
            return True
        else:
            return False

class Simulation:

    def __init__(self):
        self.persons = []

    def populate(self, n: int):
        self.persons = [Person() for i in range(n)]
        for person in self.persons:
            if random() < starting_illness_probability:
                person.infect()

    def simulate(self):
        for person in self.persons:
            person.move()
            person.simulate_illness()
            for second_person in self.persons:
                if euclides_dist((second_person.x_pos, second_person.y_pos), (person.x_pos, person.y_pos)) < spreading_radius:
                    if random() < spreading_probability and person.state == HealthState.HEALTHY and second_person.is_infecting():
                        person.infect()

    def get_persons(self):
        return self.persons


def euclides_dist(pos_a: Tuple[float, float], pos_b: Tuple[float, float]) -> float:
    return sqrt((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)


class SimulationBoard():

    def __init__(self):
        pygame.init()
        self.FPS = 24  # frames per second setting
        self.fpsClock = pygame.time.Clock()
        # definiowanie okna gry
        self.window = pygame.display.set_mode((500, 500))
        # wyświetlanie okna gry
        pygame.display.set_caption("Simulation")
        self.colors = health_state_colors()

    def clear_board(self):
        self.window.fill((255, 255, 255))

    def draw(self, person: Person):
        pygame.draw.circle(self.window, self.colors[person.state], (person.x_pos*5, person.y_pos*5), 8, 0)

    def update_board(self):
        pygame.display.update()
        self.fpsClock.tick(self.FPS)

if __name__=="__main__":
    colors = health_state_colors()
    simulation = Simulation()
    simulation.populate(n=60)
    board = SimulationBoard()
    run = True
    # pętla główna
    while run:
        # win.fill((255, 255, 255))
        # obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # funkcja rysująca kwadrat
        board.clear_board()
        persons = simulation.get_persons()
        for person in persons:
            board.draw(person)
        board.update_board()
            # pygame.draw.circle(win, (128, 0, 128), (60, 200), 50, 0)
        # y_positions = [person.y_pos for person in persons]
    #     pygame.display.update()
        simulation.simulate()
    #     # sleep(0.01)
    #     # fpsClock.tick(FPS)
    # draw(simulation.get_persons())
