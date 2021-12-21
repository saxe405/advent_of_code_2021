from typing import Dict, List

from input_parser import get_input
from dataclasses import dataclass
from collections import Counter


@dataclass
class Polymer:
    start: str
    relations: Dict[str, str]
    pairs_counter: Dict[str, int]

    def score_1(self) -> int:
        element_counter = {x: 0 for x in set(''.join(self.relations.keys()))}
        for pair, count in self.pairs_counter.items():
            element_counter[pair[0]] += count
        element_counter[self.start[-1]] +=1

        return max(element_counter.values()) - min(element_counter.values())

    def take_a_step(self) -> "Polymer":
        new_counter = {x: 0 for x in self.relations.keys()}
        for pair, count in self.pairs_counter.items():
            if count == 0:
                continue
            new_char = self.relations[pair]
            pair1 = f'{pair[0]}{new_char}'
            pair2 = f'{new_char}{pair[1]}'
            new_counter[pair1] += count
            new_counter[pair2] += count
        return Polymer(relations=self.relations, pairs_counter=new_counter, start=self.start)


def create_polymer_from_input(state: str, relations_list: List[str]) -> Polymer:
    relations = {}
    pair_counter = Counter([''.join(p) for p in zip(state, state[1:])])
    for r in relations_list:
        a, b = r.rstrip('\n').split(' -> ')
        relations[a] = b
    return Polymer(pairs_counter=pair_counter, relations=relations, start=state)


if __name__ == '__main__':
    day = int(__file__.split('/')[-1].split('_')[-1].split('.')[0])
    input_list = get_input(day=day)

    polymer = create_polymer_from_input(state=input_list[0].rstrip('\n'), relations_list=input_list[2:])
    n_steps = 40
    for _ in range(n_steps):
        polymer = polymer.take_a_step()

    print(f'Score after {n_steps} is {polymer.score_1()}')
