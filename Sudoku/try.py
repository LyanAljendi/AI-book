from queue import PriorityQueue
import numpy as np


class EmptyCell:
    def __init__(self, i, j):
        self.i = i      # line
        self.j = j      # column
        self.DOF = 9    # degree of freedom, will be updated in set_DOF
        # will be updated in set_DOF
        self.is_valid = np.array(
            [True, True, True, True, True, True, True, True, True])

    def __lt__(self, other):
        return self.DOF < other.DOF

    def __eq__(self, other):
        return self.DOF == other.DOF


if __name__ == "__main__":
    q = PriorityQueue()
    c = EmptyCell(0, 0)
    c1 = EmptyCell(1, 0)
    c2 = EmptyCell(2, 0)
    c1.DOF = 1
    c2.DOF = 2
    c.DOF = 3
    q.put(c)
    q.put(c1)
    q.put(c2)
    for cell in q.queue:
        print(cell.DOF)

    del q.queue[1]
    q.put(c)
    while not q.empty():
        print(q.get().DOF)
