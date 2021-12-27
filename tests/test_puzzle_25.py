import unittest
import numpy as np

from puzzle_25 import Floor


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_input = [
            'v...>>.vv>',
            '.vv>>.vv..',
            '>>.>v>...v',
            '>>v>>.>.v.',
            'v>v.vv.v..',
            '>.>>..v...',
            '.vv..>.>v.',
            'v.v..>>v.v',
            '....v..v.>',
        ]

    def test_example1(self):
        rights = np.array([ [int(y == '>') for y in l] for l in self.test_input])
        downs = np.array([[int(y == 'v') for y in l] for l in self.test_input])
        floor = Floor(rights=rights, downs=downs)
        n_steps = floor.number_of_steps_till_no_movement()
        self.assertEqual(n_steps, 58)

    def test_example2(self):
        pass


if __name__ == '__main__':
    unittest.main()
