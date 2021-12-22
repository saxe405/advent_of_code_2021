import numpy as np

mapping = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def convert_hex_to_bin(hex_value: str) -> str:
    return ''.join([mapping[x] for x in hex_value])


def convert_bin_to_dec(bin_value: str) -> int:
    bin_value_int = np.array([int(x) for x in bin_value])
    coeffs = np.array([2 ** (len(bin_value) - b - 1) for b in range(len(bin_value))])
    return int(np.sum(bin_value_int * coeffs))
