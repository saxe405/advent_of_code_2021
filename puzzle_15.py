from typing import List
from input_parser import get_input
import numpy as np
import heapq


class Cavern:
    def __init__(self, risk_matrix: np.array) -> None:
        self.V = [(x, y) for x in range(risk_matrix.shape[0]) for y in range(risk_matrix.shape[1])]
        self.risk_matrix = risk_matrix

    def dijkstra(self) -> int:
        dist_heap = [(0, 0, 0)]

        dist = {x: np.Inf for x in self.V}
        heapq.heapify(dist_heap)

        sptSet = {x: False for x in self.V}

        while len(dist_heap) > 0:

            risk, row, col = heapq.heappop(dist_heap)

            x = (row, col)
            if sptSet[x]:
                continue

            sptSet[x] = True
            dist[x] = risk

            adjacent_vertices = [(x[0] - 1, x[1]), (x[0] + 1, x[1]), (x[0], x[1] - 1), (x[0], x[1] + 1)]
            adjacent_vertices = [(x[0], x[1]) for x in adjacent_vertices if
                                 0 <= x[0] < self.risk_matrix.shape[0] and 0 <= x[1] < self.risk_matrix.shape[1]]
            for y in adjacent_vertices:
                new_risk = self.risk_matrix[y]
                heapq.heappush(dist_heap, (risk + new_risk, y[0], y[1]))

        return dist[self.risk_matrix.shape[0] - 1, self.risk_matrix.shape[1] - 1]


def compute_big_risk_matrix(risk_matrix: np.array) -> np.array:
    big_risk_matrix = np.block([
        [risk_matrix, risk_matrix + 1, risk_matrix + 2, risk_matrix + 3, risk_matrix + 4],
        [risk_matrix + 1, risk_matrix + 2, risk_matrix + 3, risk_matrix + 4, risk_matrix + 5],
        [risk_matrix + 2, risk_matrix + 3, risk_matrix + 4, risk_matrix + 5, risk_matrix + 6],
        [risk_matrix + 3, risk_matrix + 4, risk_matrix + 5, risk_matrix + 6, risk_matrix + 7],
        [risk_matrix + 4, risk_matrix + 5, risk_matrix + 6, risk_matrix + 7, risk_matrix + 8],
    ])
    rescaling_f = np.vectorize(lambda x: x if x <= 9 else (x - 9))
    return rescaling_f(big_risk_matrix)


if __name__ == '__main__':
    day = int(__file__.split('/')[-1].split('_')[-1].split('.')[0])
    input_list = get_input(day=day)

    risk_matrix = np.array([[int(y) for y in x.rstrip('\n')] for x in input_list])
    version = 2
    if version == 1:
        cavern = Cavern(risk_matrix=risk_matrix)
        result = cavern.dijkstra()
    else:
        big_risk_matrix = compute_big_risk_matrix(risk_matrix)
        cavern = Cavern(risk_matrix=big_risk_matrix)
        result = cavern.dijkstra()

    print(f'found the least risk path of {result}')
