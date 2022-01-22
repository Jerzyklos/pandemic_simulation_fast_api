from fast_api.person import Person
from typing import List
from fast_api.base_models import SimulationParametersModel


# Data parser for parsing data from simulation to
# json format for MongoDB
class DataParser:

    def __init__(self):
        pass

    def parse_statistics(self, step, persons: List[Person]):
        data = {}
        data["step"] = step
        for person in persons:
            if person.state.value not in data:
                data[person.state.value] = 0
            else:
                data[person.state.value] += 1
        return data

    def parse_persons(self, step, persons: List[Person]):
        key = str(step)
        data = {key: []}
        for person in persons:
            data[key].append({"x": int(person.x_pos), "y": int(person.y_pos), "state": person.state.value})
        return data

    def parse_parameters(self, parameters: SimulationParametersModel):
        # change base model to json
        return parameters.dict()
