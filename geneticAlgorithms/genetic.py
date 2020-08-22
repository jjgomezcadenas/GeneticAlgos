# File: genetic.py


import random
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence, Callable, Any


@dataclass
class Chromosome:
    genes   : List
    fitness : Any


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
