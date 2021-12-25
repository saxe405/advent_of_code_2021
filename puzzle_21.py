from typing import NamedTuple

from input_parser import get_input
from dataclasses import dataclass, replace


class GameState(NamedTuple):
    player_1_position_index: int
    player_2_position_index: int
    player_1_score: int
    player_2_score: int

    def winner_exists(self) -> bool:
        return self.player_1_score >= 21 or self.player_2_score >= 21

    def player_one_wins(self) -> bool:
        return self.player_1_score >= 21

    def player_two_wins(self) -> bool:
        return self.player_2_score >= 21 and self.player_1_score < 21


@dataclass
class Winnings:
    player_1: int
    player_2: int


@dataclass
class DiracDiceDeterministic:
    player_1_position_index: int
    player_2_position_index: int
    player_1_score: int = 0
    player_2_score: int = 0
    turn: int = 1
    last_roll: int = 0

    def __init__(self, player_1_position: int, player_2_position: int):
        self.player_1_position_index = player_1_position - 1
        self.player_2_position_index = player_2_position - 1

    def play_one_step(self) -> None:
        if self.turn == 1:
            self.turn = 2
            self.player_1_position_index = (3 * self.last_roll + 6 + self.player_1_position_index) % 10
            self.player_1_score += self.player_1_position_index + 1
        else:
            self.turn = 1
            self.player_2_position_index = (3 * self.last_roll + 6 + self.player_2_position_index) % 10
            self.player_2_score += self.player_2_position_index + 1
        self.last_roll += 3

    def player_1_wins(self) -> bool:
        return self.player_1_score >= 1000

    def player_2_wins(self) -> bool:
        return self.player_2_score >= 1000

    def winner_exists(self) -> bool:
        return self.player_1_wins() or self.player_1_wins()


def part_one():
    board = DiracDiceDeterministic(player_1_position=10, player_2_position=6)
    while True:
        board.play_one_step()
        if board.winner_exists():
            break
    loser_scorer = board.player_1_score if board.player_2_wins() else board.player_2_score
    print(f'{loser_scorer * board.last_roll}')


def part_two():
    all_combinations = dict()
    for p1 in range(10):
        for p2 in range(10):
            for s1 in range(22):
                for s2 in range(22):
                    this_combination = GameState(player_1_score=s1,
                                                 player_2_score=s2,
                                                 player_1_position_index=p1,
                                                 player_2_position_index=p2)
                    all_combinations[this_combination] = 0
    all_combinations[GameState(player_1_score=0, player_2_score=0,
                               player_1_position_index=10 - 1, player_2_position_index=6 - 1)] = 1
    winnings = Winnings(player_1=0, player_2=0)
    roll_combinations = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

    while not max(all_combinations.values()) == 0:
        for game_state, num_universe_in_state in all_combinations.items():
            if num_universe_in_state > 0:
                for roll_player_1 in roll_combinations:
                    for roll_player_2 in roll_combinations:
                        player_1_position_index = (game_state.player_1_position_index + roll_player_1[0]) % 10
                        player_1_score = game_state.player_1_score + player_1_position_index + 1

                        player_2_position_index = (game_state.player_2_position_index + roll_player_2[0]) % 10
                        player_2_score = game_state.player_2_score + player_2_position_index + 1
                        new_state = game_state._replace(player_2_position_index=player_2_position_index,
                                                        player_2_score=player_2_score,
                                                        player_1_position_index=player_1_position_index,
                                                        player_1_score=player_1_score)
                        if new_state.player_one_wins():
                            winnings.player_1 += num_universe_in_state * roll_player_1[1]
                            break
                        elif new_state.player_two_wins():
                            winnings.player_2 += num_universe_in_state * roll_player_1[1] * roll_player_2[1]
                        elif not new_state.winner_exists():
                            all_combinations[new_state] += num_universe_in_state * roll_player_1[1] * roll_player_2[1]
                all_combinations[game_state] = 0
    print(winnings)
    print(max(winnings.player_1, winnings.player_2))


if __name__ == '__main__':
    part_two()
