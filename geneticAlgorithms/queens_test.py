from pytest import fixture
import numpy as np

from geneticAlgorithms.genetic import Chromosome
from geneticAlgorithms.genetic import mutate_chromosome
from geneticAlgorithms.genetic import generate_parent

from geneticAlgorithms.Queens import Board
from geneticAlgorithms.Queens import get_fitness



def test_diagonal_board():
    sizeBoard = 8
    geneTest = np.arange(sizeBoard)
    print(geneTest)

    bTest = Board(geneTest)
    bTest.display_board()

    counter = 0
    for i,j in list(zip(np.arange(sizeBoard), np.arange(sizeBoard))):
        if bTest.board[i,j] == 1:
            counter += 1

    assert counter == sizeBoard


# Hector
def test_columns_board():
    return True


def test_diagonal_fitness_equals_25():
    geneTest = np.arange(8)
    assert get_fitness(geneTest) == 25


# Hector: add a test for fitness of a matrix with first column = 1 all
# the rest equals to zero.

# Hector: add a test for fitness of a matrix with i column = 1 all
# the rest equals to zero, where now, i = (0,1,2...7)

# Hector: add a test for this configuration

# . . . . Q . . .
# . . Q . . . . .
# Q . . . . . . .
# . . . . . . Q .
# . Q . . . . . .
# . . . . . . . Q
# . . . . . Q . .
# . . . Q . . . .


# Hector: Make the run in Queens.py a test. Check that
# we find solutions for different sizes.
# What is the minimum size at which we find solutions?
# How does the speed of the algorithm scale with size of board (9,10...)?
