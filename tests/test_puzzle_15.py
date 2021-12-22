import unittest
import numpy as np

from puzzle_15 import compute_big_risk_matrix, Cavern


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_input = np.array([
            [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
            [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
            [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
            [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
            [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
            [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
            [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
            [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
            [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
            [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]
        ])

    def test_example1(self):
        cavern = Cavern(risk_matrix=self.test_input)
        result = cavern.dijkstra()
        self.assertEqual(result, 40)

    def test_example_bigger_size(self):
        big_risk_matrix = compute_big_risk_matrix(self.test_input)
        cavern = Cavern(risk_matrix=big_risk_matrix)
        result = cavern.dijkstra()
        self.assertEqual(result, 315)


if __name__ == '__main__':
    unittest.main()
