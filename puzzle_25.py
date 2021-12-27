import dataclasses

from input_parser import get_input
import numpy as np


@dataclasses.dataclass
class Floor:
    rights: np.array
    downs: np.array

    @property
    def any_cucumber_exists(self) -> np.ndarray:
        return (self.rights + self.downs) > 0

    @property
    def right_cucumber_exists(self) -> np.ndarray:
        return self.rights > 0

    @property
    def down_cucumber_exists(self) -> np.ndarray:
        return self.downs > 0

    # rights then downs
    def take_one_step_right(self) -> "Floor":
        cucumber_positions = self.any_cucumber_exists
        cucumber_blocking = np.block([cucumber_positions[:, 1:], cucumber_positions[:, 0:1]])
        new_rights = np.roll(self.right_cucumber_exists & ~cucumber_blocking, 1, axis=1)
        new_rights[cucumber_blocking & self.right_cucumber_exists] = 1

        return Floor(downs=self.downs, rights=new_rights.astype(int))

    def take_one_step_down(self) -> "Floor":
        cucumber_positions = self.any_cucumber_exists
        cucumber_blocking = np.block([[cucumber_positions[1:, :]], [cucumber_positions[0:1, :]]])
        new_downs = np.roll(self.down_cucumber_exists & ~cucumber_blocking, 1, axis=0)
        new_downs[cucumber_blocking & self.down_cucumber_exists] = 1
        return Floor(downs=new_downs.astype(int), rights=self.rights)

    def take_one_complete_step(self) -> "Floor":
        post_right = self.take_one_step_right()
        post_down = post_right.take_one_step_down()
        return post_down

    def __repr__(self) -> str:
        repr_str = ''
        for i in range(self.downs.shape[0]):
            new_str = ''
            for j in range(self.rights.shape[1]):
                if self.rights[i, j] > 0:
                    new_str += '>'
                elif self.downs[i, j] > 0:
                    new_str += 'v'
                else:
                    new_str += '.'
            repr_str += new_str + '\n'
        return repr_str

    def __eq__(self, other: "Floor") -> bool:
        return np.all(self.downs == other.downs) and np.all(self.rights == other.rights)

    def number_of_steps_till_no_movement(self) -> int:
        n_steps = 1
        current_floor = self.take_one_complete_step()
        while True:
            new_floor = current_floor.take_one_complete_step()
            n_steps += 1
            if current_floor == new_floor:
                return n_steps

            current_floor = new_floor


if __name__ == '__main__':
    day = int(__file__.split('/')[-1].split('_')[-1].split('.')[0])
    input_list = get_input(day=day)

    rights = np.array([[int(y == '>') for y in l.rstrip('\n')] for l in input_list])
    downs = np.array([[int(y == 'v') for y in l.rstrip('\n')] for l in input_list])
    floor = Floor(rights=rights, downs=downs)
    n_steps = floor.number_of_steps_till_no_movement()
    print(f'Num steps to no movement {n_steps}')