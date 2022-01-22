import pygame
from fast_api.person import Person
from fast_api.simulation_parameters import HealthState
from typing import Dict


def health_state_colors() -> Dict[HealthState, pygame.Color]:
    colors = {}
    colors[HealthState.HEALTHY] = pygame.Color("green")
    colors[HealthState.SYMPTOMATIC] = pygame.Color("red")
    colors[HealthState.ASYMPTOMATIC] = pygame.Color("yellow")
    colors[HealthState.DEAD] = pygame.Color("black")
    return colors


# Board used to display simulation, is used when
# display_board is True
class SimulationBoard():

    def __init__(self):
        pygame.init()
        self.FPS = 24
        self.fpsClock = pygame.time.Clock()
        self.window = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Simulation")
        self.colors = health_state_colors()

    def is_closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def clear_board(self):
        self.window.fill((255, 255, 255))

    def draw(self, person: Person):
        pygame.draw.circle(self.window, self.colors[person.state], (person.x_pos*5, person.y_pos*5), 8, 0)

    def update_board(self):
        pygame.display.update()
        self.fpsClock.tick(self.FPS)
