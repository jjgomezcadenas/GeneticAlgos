# File: helloWorld.py

import random
import datetime
from dataclasses import dataclass

import numpy as np

from typing import List, Dict, Tuple, Sequence

from geneticAlgorithms.genetic import Chromosome
from geneticAlgorithms.genetic import mutate_chromosome
from geneticAlgorithms.genetic import generate_parent
from geneticAlgorithms.genetic import optimize  


@dataclass
class Board:
    genes  : List

    def __post_init__(self):
        self.sizeBoard = int(len(self.genes))
        self.board = self.define_board(self.genes, self.sizeBoard)

    def define_board(self, genes: List, sizeBoard: int)->np.array:
        x = np.arange(sizeBoard * sizeBoard)
        x = x.reshape(sizeBoard,  sizeBoard)
        board = np.zeros_like(x)

        # rows are always defined from (0,size), thus permutation
        # (mutations) occur in columns.
        # This cuts symmetric solutions in rows/columns

        R = np.arange(0, sizeBoard)
        for i in np.arange(0, sizeBoard):
            column = genes[i]  # columns defined by genes (indexes)
            row = R[i]
            board[row][column] = 1
        return board

    def display_board(self):
        print(self.board)


def get_fitness(genes):
    """The fitness function proceeds like this:
    1. Finds the queens present in each row, column, north and south diagonals.
       If more than one queen is present, we ignore the repetitions,
       since a single Queen covers
       the full line (row, column or diagonal)
    2. Assign a fitness value to each line equal to the size of the Board
       minus the length of the set.
    3. Add the four lines.
    4. Substract the fitness from the maximum fitness (4 * size of board)

    With an example:

    . . . . Q . . .
    . . Q . . . . .
    Q . . . . . . .
    . . . . . . Q .
    . Q . . . . . .
    . . . . . . . Q
    . . . . . Q . .
    . . . Q . . . .

    count for Rows = {0,1,2,3,4,5,6,7}  --> len(Row) = 8 fitness_Row = 8 - 8 = 0
    count for Cols = {0,1,2,3,4,5,6,7}  --> len(Row) = 8 fitness_Row = 8 - 8 = 0
    count for NDia = {3,4,5,6,8,9,10,11}--> len(Row) = 8 fitness_Row = 8 - 8 = 0
    count for SDia = {2,3,4,5,9,10,11,12}-> len(Row) = 8 fitness_Row = 8 - 8 = 0

    total count = 0

    total fitness = 8 *4 = 32

    """
    def partial_fitness(size, mset):
        return size - len(mset)

    b = Board(genes)

    size  = b.sizeBoard
    rQ    = set()  #use sets to avoid double counting
    cQ    = set()
    nDQ   = set()
    sDQ   = set()

    for row in range(size):
        for col in range(size):
            if b.board[row,col] == 1:
                rQ .add(row)
                cQ .add(col)
                nDQ.add(row + col)
                sDQ.add(size - 1 - col + row)

    total = partial_fitness(size,rQ) + partial_fitness(size, cQ) + \
            partial_fitness(size, nDQ) + partial_fitness(size, sDQ)

    return 4 * size - total


def compare_fitness(f1, f2):
    return f1 >= f2



if __name__ == "__main__":

    sizeBoard      = 8
    optimalFitness = 4 * sizeBoard
    geneSet = [i for i in range(sizeBoard)]
    print(f'gene set = {geneSet}')
    i, time, solve = optimize(sizeBoard, geneSet,
                              get_fitness, compare_fitness, optimalFitness,
                              verbose=True, imax=10000)
    b = Board(solve.genes)

    print(f"""iteration = {i},
              time      = {time},
              genotype  = {solve}
              fenotype  : \n {b.board}
              """ )
