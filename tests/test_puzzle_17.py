import unittest

from puzzle_17 import starting_probe_state, find_max_height_velocity, find_number_of_successful_velocities


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_input = "target area: x=20..30, y=-10..-5"

    def test_example1(self):
        probe_state = starting_probe_state(self.test_input)
        result = find_max_height_velocity(probe_state)
        self.assertEqual(result.max_height, 45)
        self.assertEqual(result.velocity_y, 9)
        self.assertEqual(result.velocity_x, 6)

    def test_example2(self):
        probe_state = starting_probe_state(self.test_input)
        n_successful_vels = find_number_of_successful_velocities(probe_state)
        self.assertEqual(n_successful_vels, 112)


if __name__ == '__main__':
    unittest.main()