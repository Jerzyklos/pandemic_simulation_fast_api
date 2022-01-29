from random import random
from typing import Tuple
from math import sqrt
from fast_api.backend.person import Person
from fast_api.backend.simulation_board import SimulationBoard
from fast_api.backend.data_parser import DataParser
from fast_api.backend.database_connection import MongoDB
# all the simulation parameters
from fast_api.backend.simulation_parameters import HealthState


class Simulation:

    def __init__(self):
        self.persons = []
        self.data_parser = DataParser()
        self.mongoDB = MongoDB()
        # clear old results before launching new
        self.mongoDB.delete_collection_content()
        # get simulation parameters
        self.parameters = self.mongoDB.return_parameters()[0]

    def populate(self, n: int):
        self.persons = [Person(self.parameters) for i in range(n)]
        for person in self.persons:
            if random() < self.parameters["starting_illness_probability"]:
                person.infect()

    def simulate(self):
        for person in self.persons:
            person.move()
            person.simulate_illness()
            if person.state != HealthState.DEAD:
                for second_person in self.persons:
                    if euclides_dist((second_person.x_pos, second_person.y_pos), (person.x_pos, person.y_pos)) < self.parameters["spreading_radius"]:
                        if random() < self.parameters["spreading_probability"] and person.state == HealthState.HEALTHY and second_person.is_infecting():
                            person.infect()

    def write_data_to_DB(self, step):
        # interval of statistics
        interval_stats = 10
        if step % interval_stats == 0:
            statistics = self.data_parser.parse_statistics(step, self.persons)
            self.mongoDB.add_stats_to_col(statistics)
        # info about persons positions and states
        # interval of writing persons positions and state
        interval_persons = 100
        if step % interval_persons == 0:
            persons_info = self.data_parser.parse_persons(step, self.persons)
            self.mongoDB.add_persons_to_col(persons_info)

    def get_persons(self):
        return self.persons


def euclides_dist(pos_a: Tuple[float, float], pos_b: Tuple[float, float]) -> float:
    return sqrt((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)


def run_simulation(population: int):
    display_board = False
    simulation = Simulation()
    simulation.populate(population)
    if display_board:
        board = SimulationBoard()
    # simulation main loop
    step = 0
    max_steps = simulation.parameters["simulation_steps"]
    while step < max_steps:
        simulation.simulate()
        simulation.write_data_to_DB(step)
        step += 1
        if step % 1000 == 0:
            print("Simulation steps: {}".format(step))
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


if __name__=="__main__":
    run_simulation(30)
