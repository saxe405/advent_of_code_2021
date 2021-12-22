import unittest

from num_conversion_utilities import convert_hex_to_bin
from puzzle_16 import Packet


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_example1(self):
        test_input = 'D2FE28'
        packet = Packet(packet_bin=convert_hex_to_bin(test_input))
        sum_version_numbers = packet.sum_of_version_numbers(0)[1]
        self.assertEqual(sum_version_numbers, 6)

    def test_example2(self):
        test_input = '38006F45291200'
        packet = Packet(packet_bin=convert_hex_to_bin(test_input))
        sum_version_numbers = packet.sum_of_version_numbers(0)[1]
        self.assertEqual(sum_version_numbers, 1 + 6 + 2)

    def test_example3(self):
        test_input = 'EE00D40C823060'
        packet = Packet(packet_bin=convert_hex_to_bin(test_input))
        sum_version_numbers = packet.sum_of_version_numbers(0)[1]
        self.assertEqual(sum_version_numbers, 7 + 2 + 4 + 1)

    def test_example4(self):
        test_inputs = ['8A004A801A8002F478', '620080001611562C8802118E34', 'C0015000016115A2E0802F182340',
                       'A0016C880162017C3686B18A3D4780']
        expected_results = [16, 12, 23, 31]
        for i in range(4):
            packet = Packet(packet_bin=convert_hex_to_bin(test_inputs[i]))
            sum_version_numbers = packet.sum_of_version_numbers(0)[1]
            self.assertEqual(sum_version_numbers, expected_results[i])

    def test_value_of_expression(self):
        tests = {'C200B40A82': 3, '04005AC33890': 54, '880086C3E88112': 7, 'CE00C43D881120': 9, 'D8005AC2A8F0': 1,
                 'F600BC2D8F': 0, '9C005AC2F8F0': 0, '9C0141080250320F1802104A08': 1}
        for pack, value in tests.items():
            packet = Packet(packet_bin=convert_hex_to_bin(pack))
            value_of_expression = packet.value_of_expression(0)[1]
            self.assertEqual(value_of_expression, value)


if __name__ == '__main__':
    unittest.main()
