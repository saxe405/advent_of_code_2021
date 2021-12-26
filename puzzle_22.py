from typing import NamedTuple, Tuple, Optional, List

import numpy as np

from input_parser import get_input
import re


class TargetRegion(NamedTuple):
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]


class Instruction(NamedTuple):
    on: bool  # for off this is false
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]

    def volume(self) -> int:
        s = 1 if self.on else -1
        volume = s * (self.x[1] - self.x[0] + 1) * (self.y[1] - self.y[0] + 1) * (self.z[1] - self.z[0] + 1)
        return volume

    def reduce_to_target_region(self, target_region: Optional[TargetRegion]) -> Optional["Instruction"]:
        if target_region is None:
            return self
        x = (max(self.x[0], target_region.x[0]), min(self.x[1], target_region.x[1]))
        y = (max(self.y[0], target_region.y[0]), min(self.y[1], target_region.y[1]))
        z = (max(self.z[0], target_region.z[0]), min(self.z[1], target_region.z[1]))

        if x[0] > x[1] or y[0] > y[1] or z[0] > z[1]:
            return None
        return Instruction(on=self.on, x=x, y=y, z=z)

    def execute(self, grid: np.array, target_region: TargetRegion) -> np.array:
        new_state = 1 if self.on else 0
        grid[self.x[0] - target_region.x[0]: self.x[1] - target_region.x[0] + 1,
        self.y[0] - target_region.y[0]: self.y[1] - target_region.y[0] + 1,
        self.z[0] - target_region.z[0]: self.z[1] - target_region.z[0] + 1] = new_state
        return grid

    def is_overlapping(self, cuboid: "Instruction") -> bool:
        if self.x[0] > cuboid.x[1] or cuboid.x[0] > self.x[1]:
            return False
        if self.y[0] > cuboid.y[1] or cuboid.y[0] > self.y[1]:
            return False
        if self.z[0] > cuboid.z[1] or cuboid.z[0] > self.z[1]:
            return False
        return True

    def get_intersection(self, cuboid: "Instruction") -> "Instruction":
        x_region = (max(self.x[0], cuboid.x[0]), min(self.x[1], cuboid.x[1]))
        y_region = (max(self.y[0], cuboid.y[0]), min(self.y[1], cuboid.y[1]))
        z_region = (max(self.z[0], cuboid.z[0]), min(self.z[1], cuboid.z[1]))
        return Instruction(x=x_region, y=y_region, z=z_region, on=not cuboid.on)


def parse_line(line_str: str) -> Instruction:
    line_pattern = r'(\w{2,3}) [x].(.?\d+)\.\.(.?\d+),[y].(.?\d+)\.\.(.?\d+),[z].(.?\d+)\.\.(.?\d+)'
    matches = re.search(line_pattern, line_str)
    return Instruction(on=matches.group(1) == 'on',
                       x=(int(matches.group(2)), int(matches.group(3))),
                       y=(int(matches.group(4)), int(matches.group(5))),
                       z=(int(matches.group(6)), int(matches.group(7))))


def count_on_cubes(input_list: List[Instruction], target_region: TargetRegion) -> int:
    parsed_lines = [l.reduce_to_target_region(target_region) for l in input_list]
    grid = np.zeros(shape=(target_region.x[1] * 2 + 1, target_region.y[1] * 2 + 1, target_region.z[1] * 2 + 1))
    for instruct in parsed_lines:
        if instruct is None:
            continue
        grid = instruct.execute(grid, target_region)
    return int(np.sum(grid))


def solve_part_one(parsed_lines: List[Instruction]) -> int:
    target_region = TargetRegion(x=(-50, 50), y=(-50, 50), z=(-50, 50))
    return count_on_cubes(parsed_lines, target_region)


def solve_part_two(parsed_lines: List[Instruction]) -> int:
    cuboids = []
    for instruction in parsed_lines:
        intersections = []
        for cuboid in cuboids:
            if cuboid.is_overlapping(instruction):
                intersection = instruction.get_intersection(cuboid)
                intersections.append(intersection)

        cuboids = cuboids + intersections
        if instruction.on:
            cuboids.append(instruction)

    return sum([x.volume() for x in cuboids])


if __name__ == '__main__':
    day = int(re.search(r'.+(\d\d)\.py$', __file__).group(1))
    input_list = get_input(day=day)

    parsed_lines = [parse_line(l.rstrip('\n')) for l in input_list]
    print(solve_part_one(parsed_lines))
    print(solve_part_two(parsed_lines))
