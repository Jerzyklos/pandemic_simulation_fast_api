import unittest
from main import Person, HealthState
from simulation_parameters import X_DIM, Y_DIM, quarantine

# Testing functions of Person class
class TestPerson(unittest.TestCase):

    def test_is_infecting(self):
        person = Person()
        person.state = HealthState.SYMPTOMATIC
        person.quarantined = False
        self.assertEqual(person.is_infecting(), True)
        person.quarantined = True
        quarantine = True
        self.assertEqual(person.is_infecting(), False)
        person.quarantined = False
        person.state = HealthState.HEALTHY
        self.assertEqual(person.is_infecting(), False)

    def test_move(self):
        person = Person()
        person.x_pos = 5
        person.y_pos = 5
        person.x_velocity = 2
        person.y_velocity = 2
        person.move()
        self.assertEqual(person.x_pos, 7)
        self.assertEqual(person.y_pos, 7)
        # test bouncing of edges
        person.x_pos = X_DIM-1
        person.y_pos = Y_DIM-1
        person.x_velocity = 2
        person.y_velocity = 2
        person.move()
        self.assertEqual(person.x_pos, X_DIM)
        self.assertEqual(person.x_velocity, -2)
        self.assertEqual(person.y_pos, Y_DIM)
        self.assertEqual(person.y_velocity, -2)

    def test_infect(self):
        person = Person()
        person.state = HealthState.HEALTHY
        person.infect()
        self.assertEqual(
            (person.state == HealthState.SYMPTOMATIC or person.state == HealthState.ASYMPTOMATIC), True)

if __name__ == '__main__':
    unittest.main()
