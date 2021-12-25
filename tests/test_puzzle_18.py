import unittest

from puzzle_18 import compute_sf_number, add_sf_numbers, reduce_sf_number


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_input_1 = [
            '[1, 1]',
            '[2, 2]',
            '[3, 3]',
            '[4, 4]',
            '[5, 5]',
            '[6, 6]'
        ]
        self.test_input_2 = [
            '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
            '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
            '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
            '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
            '[7,[5,[[3,8],[1,4]]]]',
            '[[2,[2,2]],[8,[8,1]]]',
            '[2,9]',
            '[1,[[[9,3],9],[[9,0],[0,7]]]]',
            '[[[5,[7,4]],7],1]',
            '[[[[4,2],2],6],[8,7]]',
        ]

    def test_example1(self):
        result = compute_sf_number(self.test_input_1[0])
        for i in range(1, len(self.test_input_1)):
            num2 = compute_sf_number(self.test_input_1[i])
            result = add_sf_numbers(result, num2)
            result = reduce_sf_number(result)
        self.assertEqual(result, compute_sf_number('[[[[5,0],[7,4]],[5,5]],[6,6]]'))

    def test_example2(self):
        result = compute_sf_number(self.test_input_2[0])
        for i in range(1, len(self.test_input_2)):

            num2 = compute_sf_number(self.test_input_2[i])
            result = add_sf_numbers(result, num2)
            result = reduce_sf_number(result)
        self.assertEqual(result, compute_sf_number('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'))


if __name__ == '__main__':
    unittest.main()
