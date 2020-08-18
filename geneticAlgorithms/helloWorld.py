# File: helloWorld.py


import random
import copy
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence


@dataclass
class Chromosome:
    genes   : List
    fitness : float

    def __str__(self):
        st = f"genes = {list_to_string(self.genes)}  fitnes = {self.fitness}"
        return st

    def __repr__(self):
        return self.str()


def list_to_string(mlist : List)->str:
    return ''.join(mlist)


def string_to_list(mstr : str)->List:
    return [x for x in mstr]


def get_fitness(guess: Sequence, target: Sequence)->float:
    """Computes the fitness of the target comparing with guess:
       Both are strings: if the character in target matches character in guess,
       fitness increases by one

    """
    return sum(1 for t, g in zip(target, guess)
               if t == g)


def generate_parent(target: str, geneSet: str)->Chromosome:
    """Generates an initial chromosome"""
    genes   = random.sample(geneSet, len(target))  # A set of genes, sampled from the geneSet
    fitness = get_fitness(genes, target)           # Compare genes with target, returns a float
    return Chromosome(genes, fitness)


def mutate_genes(genes: List, geneSet: str)->List:
    """Mutate genes target choosing character from geneSet"""

    mutatedGenes         = genes[:]
    #mutatedGenes         = genes # uncomment to make test fail
    index                = random.randrange(0, len(mutatedGenes))
    newGene, alternate   = random.sample(geneSet, 2)
    mutatedGenes[index]  = alternate if newGene == mutatedGenes[index] else newGene
    return mutatedGenes


def mutate_chromosome(target: str, geneSet: str, parent: Chromosome)->Chromosome:
    """Generate a mutated chromosome"""
    mutatedGenes = mutate_genes(parent.genes, geneSet)
    fitness      = get_fitness(mutatedGenes, target)
    return Chromosome(mutatedGenes, fitness)


def compare_with_target(target: str, guess: Chromosome)->bool:
    return guess.fitness == len(target)


def guess_target(target: str, geneSet: str, imax: int = 1000000):
    random.seed()
    guess = generate_parent(target, geneSet)
    print(f'initial guess : {guess}  len(genes) ={len(guess.genes)}')

    i = 0
    while compare_with_target(target, guess) == False and i < imax:
        newGuess = mutate_chromosome(target, geneSet, guess)
        #print(f'new guess : {newGuess}, i = {i}')
        if newGuess.fitness > guess.fitness:
            guess = Chromosome(newGuess.genes, newGuess.fitness)
            print(f'new guess increased fitness : {guess}, i = {i}')
        i+=1
    return i, guess


if __name__ == "__main__":

    geneSet = " 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."
    target = "This is the World's famous password"

    startTime = datetime.datetime.now()
    i, guess = guess_target(target, geneSet)
    time = datetime.datetime.now() - startTime
    print(f'guess ={guess}, time ={time}, i = {i}')
