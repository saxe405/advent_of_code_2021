from input_parser import get_input
from dataclasses import dataclass
import math

from num_conversion_utilities import convert_bin_to_dec, convert_hex_to_bin


@dataclass
class Packet:
    packet_bin: str

    def sum_of_version_numbers(self, starting_index: int) -> (int, int):
        i = starting_index
        version_sum = convert_bin_to_dec(self.packet_bin[i:i + 3])
        type_id = convert_bin_to_dec(self.packet_bin[i + 3: i + 6])
        i += 3 + 3
        if type_id == 4:
            while True:
                i = i + 5
                if self.packet_bin[i - 5] == '0':
                    break
        else:
            length_type_id = self.packet_bin[i]
            if length_type_id == '0':
                end_of_packet = i + 15 + convert_bin_to_dec(self.packet_bin[i + 1:i + 16]) + 1
                i += 16
                while i < end_of_packet:
                    i, this_vs = self.sum_of_version_numbers(starting_index=i)
                    version_sum += this_vs
            else:
                n_packets = convert_bin_to_dec(self.packet_bin[i + 1: i + 12])
                i += 12
                for _ in range(n_packets):
                    i, this_vs = self.sum_of_version_numbers(starting_index=i)
                    version_sum += this_vs

        return i, version_sum

    def operation_from_type(self, type_id: int):
        match type_id:
            case 0:
                return sum
            case 1:
                return math.prod
            case 2:
                return min
            case 3:
                return max
            case 4:
                return lambda x: x[0]
            case 5:
                return lambda x: 1 if x[0] > x[1] else 0
            case 6:
                return lambda x: 1 if x[0] < x[1] else 0
            case 7:
                return lambda x: 1 if x[0] == x[1] else 0

    def value_of_expression(self, starting_index) -> (int, int):
        i = starting_index
        type_id = convert_bin_to_dec(self.packet_bin[i + 3: i + 6])
        i += 3 + 3
        values = []
        if type_id == 4:
            values.append(0)
            while True:
                values[0] = values[0] * 2 ** 4 + convert_bin_to_dec(self.packet_bin[i + 1:i + 5])
                i = i + 5
                if self.packet_bin[i - 5] == '0':
                    break
        else:
            length_type_id = self.packet_bin[i]
            if length_type_id == '0':
                end_of_packet = i + 15 + convert_bin_to_dec(self.packet_bin[i + 1:i + 16]) + 1
                i += 16
                while i < end_of_packet:
                    i, this_value = self.value_of_expression(starting_index=i)
                    values.append(this_value)
            else:
                n_packets = convert_bin_to_dec(self.packet_bin[i + 1: i + 12])
                i += 12
                for _ in range(n_packets):
                    i, this_value = self.value_of_expression(starting_index=i)
                    values.append(this_value)

        return i, self.operation_from_type(type_id)(values)


if __name__ == '__main__':
    day = int(__file__.split('/')[-1].split('_')[-1].split('.')[0])
    input_list = get_input(day=day)
    packets_hex = input_list[0].rstrip('\n')
    packet = Packet(packet_bin=convert_hex_to_bin(packets_hex))
    print(f'sum_version_numbers = {packet.sum_of_version_numbers(0)[1]}')
    print(f'value of expression = {packet.value_of_expression(0)[1]}')
