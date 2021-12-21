import unittest

from puzzle_14 import create_polymer_from_input


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_start_state = 'NNCB'
        self.test_relations = [
            'CH -> B',
            'HH -> N',
            'CB -> H',
            'NH -> C',
            'HB -> C',
            'HC -> B',
            'HN -> C',
            'NN -> C',
            'BH -> H',
            'NC -> B',
            'NB -> B',
            'BN -> B',
            'BB -> N',
            'BC -> B',
            'CC -> N',
            'CN -> C']

    def test_example1(self):
        polymer = create_polymer_from_input(state=self.test_start_state, relations_list=self.test_relations)
        for i in range(10):
            polymer = polymer.take_a_step()
        self.assertEqual(polymer.score_1(), 1588)

    def test_example_forty_steps(self):
        polymer = create_polymer_from_input(state=self.test_start_state, relations_list=self.test_relations)
        for i in range(40):
            print(f'at step {i + 1}')
            polymer = polymer.take_a_step()
        self.assertEqual(polymer.score_1(), 2188189693529)


if __name__ == '__main__':
    unittest.main()
