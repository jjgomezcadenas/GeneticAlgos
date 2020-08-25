from pytest import fixture
import numpy as np

from geneticAlgorithms.genetic import Chromosome
from geneticAlgorithms.genetic import mutate_chromosome
from geneticAlgorithms.genetic import generate_parent

from geneticAlgorithms.Queens import Board
from geneticAlgorithms.Queens import get_fitness
from geneticAlgorithms.Queens import compare_fitness
from geneticAlgorithms.genetic import optimize



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
    sizeBoard = 8
    geneTest = [0 for i in range(sizeBoard)]
    print(geneTest)

    bTest = Board(geneTest)
    bTest.display_board()

    counter = 0
    for i in list(np.arange(sizeBoard)):
        if bTest.board[i,0] == 1:
            counter += 1

    assert counter == sizeBoard


def test_diagonal_fitness_equals_25():
    geneTest = np.arange(8)
    assert get_fitness(geneTest) == 25


# Hector: add a test for fitness of a matrix with i column = 1 all
# the rest equals to zero, where now, i = (0,1,2...7)
def test_columns_board():
    sizeBoard = 8
    for j in list(np.arange(sizeBoard)):
        geneTest = [j for k in range(sizeBoard)]
        print(geneTest)

        bTest = Board(geneTest)
        bTest.display_board()

        counter = 0
        for i in list(np.arange(sizeBoard)):
            if bTest.board[i,j] == 1:
                counter += 1

        assert counter == sizeBoard

# Hector: add a test for this configuration
def test_no_queen_danger():
    geneTest2 = np.array([4, 2, 0, 6, 1, 7, 5, 3])
    assert get_fitness(geneTest2) == 32

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
def test_queens_py():
    sizeBoard      = 8
    optimalFitness = 4 * sizeBoard
    geneSet = [i for i in range(sizeBoard)]
    print(f'gene set = {geneSet}')
    _,_, guess = optimize(sizeBoard, geneSet,
                              get_fitness, compare_fitness, optimalFitness,
                              verbose=True, imax=10000)

    assert guess.fitness == 32
