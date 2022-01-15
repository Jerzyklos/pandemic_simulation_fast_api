from random import random, randint
from typing import Tuple
from math import sqrt
from person import Person
from simulation_board import SimulationBoard
from data_parser import DataParser
from database_connection import MongoDB
# all the simulation parameters
from simulation_parameters import *


class Simulation:

    def __init__(self):
        self.persons = []
        self.data_parser = DataParser()
        self.mongoDB = MongoDB()

    def populate(self, n: int):
        self.persons = [Person() for i in range(n)]
        for person in self.persons:
            if random() < starting_illness_probability:
                person.infect()

    def simulate(self):
        for person in self.persons:
            person.move()
            person.simulate_illness()
            if person.state != HealthState.DEAD:
                for second_person in self.persons:
                    if euclides_dist((second_person.x_pos, second_person.y_pos), (person.x_pos, person.y_pos)) < spreading_radius:
                        if random() < spreading_probability and person.state == HealthState.HEALTHY and second_person.is_infecting():
                            person.infect()

    def write_data_to_DB(self, steps):
        # interval of statistics
        interval = 10
        if steps % interval == 0:
            statistics = self.data_parser.parse_statistics(self.persons)
            self.mongoDB.add_stats_to_col(statistics)
        # info about persons positions and states
        persons_info = self.data_parser(persons)
        self.mongoDB.add_persons_to_col(persons_info)


    def get_persons(self):
        return self.persons


def euclides_dist(pos_a: Tuple[float, float], pos_b: Tuple[float, float]) -> float:
    return sqrt((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)


if __name__=="__main__":
    display_board = False
    simulation = Simulation()
    simulation.populate(n=100)
    if display_board:
        board = SimulationBoard()
    # simulation main loop
    steps = 0
    while steps < simulation_steps:
        simulation.simulate()
        simulation.write_data_to_DB(steps)
        steps += 1
        if steps % 1000 == 0:
            print("Simulation steps: {}".format(steps))
        if display_board:
            # handling of closing the board
            closed = board.is_closed()
            if closed:
                break
            board.clear_board()
            persons = simulation.get_persons()
            for person in persons:
                board.draw(person)
            board.update_board()
