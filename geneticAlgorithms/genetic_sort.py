# File: genetic.py


import random
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence, Callable


@dataclass
class Fitness:
    sortCount : int
    gap       : int


@dataclass
class Chromosome:
    genes   : List
    fitness : Fitness


def generate_parent(length:      int,
                    geneSet:     List,
                    get_fitness: Callable)->Chromosome:

    """Generates an initial chromosome:
    -genes are sampled from the geneSet
    -fitness is passed in the argument

    """

    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def mutate_genes(genes: List, geneSet: List)->List:
    """Mutate genes target choosing character from geneSet"""

    mutatedGenes         = genes[:]
    index                = random.randrange(0, len(mutatedGenes))
    newGene, alternate   = random.sample(geneSet, 2)
    mutatedGenes[index]  = alternate if newGene == mutatedGenes[index] else newGene
    return mutatedGenes


def mutate_chromosome(geneSet:     List,
                      parent:      Chromosome,
                      get_fitness: Callable)->Chromosome:
    """Generate a mutated chromosome"""
    mutatedGenes = mutate_genes(parent.genes, geneSet)
    fitness      = get_fitness(mutatedGenes)
    return Chromosome(mutatedGenes, fitness)


def get_fitness(genes : List)->Fitness:
    sortCount = 1
    gap = 0

    for i in range(1, len(genes)):
        if genes[i] > genes[i - 1]:
            sortCount += 1
        else:
            gap += genes[i - 1] - genes[i]
    return Fitness(sortCount, gap)


def compare_fitness(f1: Fitness, f2: Fitness)->bool:
    """Returns True if f1 is fitter than f2"""
    if f1.sortCount == f2.sortCount:
        return f1.gap <=f2.gap
    else:
        return f1.sortCount >= f2.sortCount
