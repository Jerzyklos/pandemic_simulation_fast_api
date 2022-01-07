import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
from enum import Enum
from random import random, randrange, randint
from typing import List, Dict, Tuple
from time import sleep
from math import sqrt

# fig, ax = plt.subplots()
#
# x = np.arange(0, 2*np.pi, 0.01)
# line, = ax.plot(x, np.sin(x))

asymptomatic_probability = 0.1
symptomatic_probability = 0.1
spreading_probability = 0.05
quarantine = False
r = 5
duration = 1000

X_DIM = 100
Y_DIM = 100

class HealthState(Enum):
    HEALTHY = "healthy"
    ASYMPTOMATIC = "asymptomatic"
    SYMPTOMATIC = "symptomatic"
    DEAD = "dead"


class Person:
    def __init__(self):
        self.state = HealthState.HEALTHY
        self.x_pos = randint(0, X_DIM)
        self.y_pos = randint(0, Y_DIM)
        self.x_velocity = -0.5+random()
        self.y_velocity = -0.5+random()
        self.illness_duration = 0
    def move(self):
        if self.state != HealthState.DEAD:
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
    def illness(self):
        if self.state != HealthState.HEALTHY and self.state != HealthState.DEAD:
            if self.illness_duration>duration:
                if random()>0.5:
                    self.state = HealthState.HEALTHY
                elif random()<0.1:
                    self.state = HealthState.DEAD
            else:
                self.illness_duration += 1


class Simulation:
    def __init__(self):
        self.persons = []
    def populate(self, n=10):
        self.persons = [Person() for i in range(n)]
        for person in self.persons:
            random_value = random()
            if random_value < asymptomatic_probability:
                person.state = HealthState.ASYMPTOMATIC
            elif random_value > symptomatic_probability and random_value < (symptomatic_probability+asymptomatic_probability):
                person.state = HealthState.SYMPTOMATIC
    def simulate(self):
        for person in self.persons:
            person.move()
            person.illness()
    def get_persons(self):
        return self.persons

def health_state_colors() -> Dict[HealthState, pygame.Color]:
    colors = {}
    colors[HealthState.HEALTHY] = pygame.Color("green")
    colors[HealthState.SYMPTOMATIC] = pygame.Color("red")
    colors[HealthState.ASYMPTOMATIC] = pygame.Color("yellow")
    colors[HealthState.DEAD] = pygame.Color("black")
    return colors

def euclides_dist(pos_a : Tuple[float, float], pos_b : Tuple[float, float]) -> float:
    return sqrt((pos_a[0]-pos_b[0])*(pos_a[0]-pos_b[0])+(pos_a[1]-pos_b[1])*(pos_a[1]-pos_b[1]))

if __name__=="__main__":
    colors = health_state_colors()
    simulation = Simulation()
    simulation.populate(n=30)
    pygame.init()
    # definiowanie okna gry
    win = pygame.display.set_mode((500, 500))
    # wyświetlanie okna gry
    pygame.display.set_caption("Moja Gra")
    run = True
    # pętla główna
    while run:
        win.fill((255, 255, 255))
        # obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # funkcja rysująca kwadrat
        persons = simulation.get_persons()
        positions = [(person.x_pos, person.y_pos) for person in persons]
        for person in persons:
            pygame.draw.circle(win, colors[person.state], (person.x_pos*5, person.y_pos*5), 8, 0)
            for second_person in persons:
                if euclides_dist((second_person.x_pos, second_person.y_pos), (person.x_pos, person.y_pos)) < r:
                    if random() < spreading_probability and person.state == HealthState.HEALTHY and (second_person.state == HealthState.ASYMPTOMATIC or second_person.state == HealthState.SYMPTOMATIC):
                        if random() < 0.5:
                            person.state = HealthState.SYMPTOMATIC
                        else:
                            person.state = HealthState.ASYMPTOMATIC
        pygame.display.update()
        simulation.simulate()
        sleep(0.01)
    
