from typing import Optional, NamedTuple

from input_parser import get_input
from dataclasses import dataclass


@dataclass
class Probe:
    position_x: int
    position_y: int
    velocity_x: int
    velocity_y: int
    target_x: (int, int)
    target_y: (int, int)
    n_steps: int
    max_height: int

    def take_one_step(self) -> None:
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y
        current_velocity_x = self.velocity_x

        # drag
        if current_velocity_x > 0:
            self.velocity_x -= 1
        elif current_velocity_x < 0:
            self.velocity_x += 1
        # gravity
        self.velocity_y -= 1
        self.n_steps += 1
        self.max_height = max(self.max_height, self.position_y)

    def reached_target_area(self) -> bool:
        within_x_range = self.target_x[0] <= self.position_x <= self.target_x[1]
        within_y_range = self.target_y[0] <= self.position_y <= self.target_y[1]
        return within_x_range and within_y_range

    def has_overshot_target_area(self) -> bool:
        too_left = self.position_x < self.target_x[0] and self.velocity_x <= 0
        too_right = self.position_x > self.target_x[1] and self.velocity_x >= 0
        too_down = self.position_y < self.target_y[0] and self.velocity_y <= 0

        return too_left or too_right or too_down

    def reset_probe(self, velocity_x: int, velocity_y: int) -> None:
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.position_x = 0
        self.position_y = 0
        self.n_steps = 0
        self.max_height = 0


def starting_probe_state(input_str: str) -> Probe:
    target_x = list(map(int, input_str.split(': ')[1].split(', ')[0].split('=')[1].split('..')))
    target_y = list(map(int, input_str.split(': ')[1].split(', ')[1].split('=')[1].split('..')))
    return Probe(position_x=0, position_y=0,
                 velocity_x=0, velocity_y=0,
                 target_x=target_x, target_y=target_y, n_steps=0, max_height=0)


class SimulationResult(NamedTuple):
    max_height: int
    velocity_y: int
    velocity_x: int


def find_max_height_velocity(probe_state: Probe) -> SimulationResult:
    result = SimulationResult(max_height=0, velocity_x=0, velocity_y=0)
    for velocity_x in range(1, probe_state.target_x[1] * 2):
        for velocity_y in range(0, abs(probe_state.target_y[1]) * 2):
            probe_state.reset_probe(velocity_x=velocity_x, velocity_y=velocity_y)
            while True:
                probe_state.take_one_step()
                if probe_state.has_overshot_target_area():
                    break
                elif probe_state.reached_target_area() and probe_state.max_height > result.max_height:
                    result = SimulationResult(max_height=probe_state.max_height,
                                              velocity_x=velocity_x,
                                              velocity_y=velocity_y)
                    break
    return result


def find_number_of_successful_velocities(probe_state: Probe) -> int:
    n_successful_vels = 0
    for velocity_x in range(1, probe_state.target_x[1] * 2):
        for velocity_y in range(min(0, probe_state.target_y[0]), abs(probe_state.target_y[1]) * 2):
            probe_state.reset_probe(velocity_x=velocity_x, velocity_y=velocity_y)
            while True:
                probe_state.take_one_step()
                if probe_state.has_overshot_target_area():
                    break
                elif probe_state.reached_target_area():
                    n_successful_vels += 1
                    break

    return n_successful_vels


if __name__ == '__main__':
    day = int(__file__.split('/')[-1].split('_')[-1].split('.')[0])
    input_list = get_input(day=day)

    probe_state = starting_probe_state(input_list[0])

    result = find_max_height_velocity(probe_state)
    print(f'best height achieved {result.max_height} using velocity {result.velocity_x, result.velocity_y}')

    print(f'number of successful velocities {find_number_of_successful_velocities(probe_state)}')

