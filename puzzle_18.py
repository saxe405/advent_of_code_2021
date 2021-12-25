from typing import Tuple, Union

from input_parser import get_input

"""This solution is not my original work and was inspired by another author
 the original solution can be found at topaz.github.io"""


def parse_tuple(it: iter) -> (int, int):
    c = next(it)
    if c == '[':
        left = parse_tuple(it)
        c = next(it)
    else:
        left, c = parse_digit(c, it)
    assert c == ','
    c = next(it)
    if c == '[':
        right = parse_tuple(it)
        c = next(it)
    else:
        right, c = parse_digit(c, it)
    assert c == ']'

    return left, right


def parse_digit(c: str, it: iter) -> (int, str):
    n = 0
    while c.isdigit():
        n *= 10
        n += int(c, 10)
        c = next(it)
    return n, c


def add_sf_numbers(sf_number_1, sf_number_2):
    new_sf_number = (sf_number_1, sf_number_2)
    return reduce_sf_number(new_sf_number)


def reduce_sf_number(sf_number):
    reduced = True
    while reduced:
        sf_number, reduced, _, _ = explode_sf_number(sf_number, level=0)
        if not reduced:
            sf_number, reduced = split_sf_number(sf_number)
    return sf_number


def explode_sf_number(sf_number: Union[Tuple, int], level: int):
    if isinstance(sf_number, int):
        return sf_number, False, 0, 0
    left, right = sf_number
    if level >= 4:
        return 0, True, left, right
    else:
        left, reduced, exploded_l, exploded_r = explode_sf_number(left, level + 1)
        if reduced:
            if exploded_r != 0:
                right = add_left(right, exploded_r)
                exploded_r = 0
        else:
            right, reduced, exploded_l, exploded_r = explode_sf_number(right, level + 1)
            if reduced:
                if exploded_l != 0:
                    left = add_right(left, exploded_l)
                    exploded_l = 0
        if reduced:
            return (left, right), True, exploded_l, exploded_r
        else:
            return sf_number, False, 0, 0


def add_left(sf_number, exploded_r):
    if isinstance(sf_number, int):
        return sf_number + exploded_r
    else:
        left, right = sf_number
        return add_left(left, exploded_r), right


def add_right(sf_number, exploded_l):
    if isinstance(sf_number, int):
        return sf_number + exploded_l
    else:
        left, right = sf_number
        return left, add_right(right, exploded_l)


def split_sf_number(sf_number: Union[Tuple, int]):
    if isinstance(sf_number, int):
        if sf_number > 9:
            return (sf_number // 2, (sf_number + 1) // 2), True
        else:
            return sf_number, False
    else:
        left, right = sf_number
        left, reduced = split_sf_number(left)
        if not reduced:
            right, reduced = split_sf_number(right)
        if reduced:
            num = (left, right)
            return num, True
        else:
            return sf_number, False


def magnitude(sf_number: Union[Tuple, int]) -> int:
    if isinstance(sf_number, int):
        return sf_number
    else:
        left, right = sf_number
        return 3 * magnitude(left) + 2 * magnitude(right)


def compute_sf_number(number_str: str):
    it = iter(number_str.replace(' ', ''))
    assert next(it) == '['
    return parse_tuple(it)


if __name__ == '__main__':
    day = int(__file__.split('/')[-1].split('_')[-1].split('.')[0])
    input_list = get_input(day=day)
    result = compute_sf_number(input_list[0])
    for i in range(1, len(input_list)):
        num2 = compute_sf_number(input_list[i])
        result = add_sf_numbers(result, num2)
        result = reduce_sf_number(result)

    print(result)
    print(magnitude(result))
    max_sum_magnitude = 0
    for i in range(len(input_list)):
        for j in range(len(input_list)):
            if i == j:
                continue
            n1 = compute_sf_number(input_list[i])
            n2 = compute_sf_number(input_list[j])
            result = add_sf_numbers(n1, n2)
            magn = magnitude(result)
            if magn > max_sum_magnitude:
                max_sum_magnitude = magn
    print(f'max magnitude {max_sum_magnitude}')
