# File: helloWorld.py

import random
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence

from geneticAlgorithms.genetic_sort import Chromosome
from geneticAlgorithms.genetic_sort import Fitness
from geneticAlgorithms.genetic_sort import mutate_chromosome
from geneticAlgorithms.genetic_sort import generate_parent
from geneticAlgorithms.genetic_sort import get_fitness
from geneticAlgorithms.genetic_sort import compare_fitness


def sort_numbers(totalNumbers, geneSet, verbose=True, imax=10000):
    startTime = datetime.datetime.now()
    random.seed()
    startTime = datetime.datetime.now()
    setToSort = generate_parent(totalNumbers, geneSet, get_fitness)
    print(f'Set to Sort = {setToSort}')

    optimalFitness = Fitness(totalNumbers, 0)

    i = 0
    while compare_fitness(setToSort.fitness, optimalFitness) == False and i < imax:
        newGuess = mutate_chromosome(geneSet, setToSort, get_fitness)
        time = datetime.datetime.now() - startTime
        if compare_fitness(newGuess.fitness, setToSort.fitness) == True:
            if verbose:
                print(f'new guess increased fitness: {setToSort}, i = {i}, time={time}')
            setToSort = Chromosome(newGuess.genes, newGuess.fitness)

        i+=1
    return i, time, setToSort
    

if __name__ == "__main__":

    geneSet = [i for i in range(100)]

    print(f'verbose run: Sort a list of 10 numbers')
    i, time, sorted = sort_numbers(10, geneSet, verbose=True, imax=10000)
    print(f'i ={i}: time ={time} sorted ={sorted}')

    print(f'Quiet run: Sort 20 numbers')
    i, time, sorted = sort_numbers(20, geneSet, verbose=False, imax=10000)
    print(f'i ={i}: time ={time} sorted ={sorted}')
