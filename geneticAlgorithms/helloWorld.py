# File: helloWorld.py

import random
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence

from geneticAlgorithms.genetic_hw import Chromosome
from geneticAlgorithms.genetic_hw import string_to_list, list_to_string
from geneticAlgorithms.genetic_hw import mutate_chromosome
from geneticAlgorithms.genetic_hw import generate_parent
from geneticAlgorithms.genetic_hw import compare_with_target


def matching_string_fitness(guess: Sequence, target: Sequence)->float:
    """Fitness function for matching strings.
       Computes the fitness of the target comparing with guess:
       if the character in target matches character in guess,
       fitness increases by one

    """
    return sum(1 for t, g in zip(target, guess)
               if t == g)


def guess_target(target: str, geneSet: str,
                 verbose: bool = True,
                 imax:    int  = 1000000):

    random.seed()
    startTime = datetime.datetime.now()
    guess = generate_parent(target, geneSet, matching_string_fitness)
    time = datetime.datetime.now() - startTime

    if verbose:
        print(f"""initial guess : {guess}
                  len(genes) ={len(guess.genes)},
                  time={time}""")

    i = 0
    while compare_with_target(target, guess) == False and i < imax:
        newGuess = mutate_chromosome(target, geneSet, guess,
                                     matching_string_fitness)

        if newGuess.fitness > guess.fitness:
            guess = Chromosome(newGuess.genes, newGuess.fitness)
            time = datetime.datetime.now() - startTime

            if verbose:
                print(f'new guess increased fitness : {guess}, i = {i}, time={time}')
        i+=1
    return i, time, guess


if __name__ == "__main__":

    geneSet = " 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."
    target = "This is the World's famous password"

    geneSet = "012"
    target = 10*["1"]

    geneSet = [0,1,2]
    target = 10*[1]

    i, time, guess = guess_target(target, geneSet)
    print(f'guess ={guess}, time ={time}, i = {i}')
