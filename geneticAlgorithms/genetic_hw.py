# File: genetic.py


import random
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence, Callable


@dataclass
class Chromosome:
    genes   : Sequence
    fitness : float

    def __str__(self):
        st = f"genes = {list_to_string(self.genes)}  fitnes = {self.fitness}"
        return st

    def __repr__(self):
        return self.str()


def list_to_string(mlist : List)->str:
    l2 = [f"{x}" for x in mlist]
    return ''.join(l2)


def string_to_list(mstr : str)->List:
    return [x for x in mstr]


def generate_parent(target: Sequence,
                    geneSet: Sequence,
                    get_fitness: Callable)->Chromosome:
    """Generates an initial chromosome:
    -genes are sampled from the geneSet
    -fitness is passed in the argument

    """
    # A set of genes, sampled from the geneSet
    #genes   = random.sample(geneSet, len(target))

    genes = []

    while len(genes) < len(target):
        sampleSize = min(len(target) - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))

    fitness = get_fitness(genes, target)
    return Chromosome(genes, fitness)


def mutate_genes(genes: List, geneSet: str)->List:
    """Mutate genes target choosing character from geneSet"""

    mutatedGenes         = genes[:]
    #mutatedGenes         = genes # uncomment to make test fail
    index                = random.randrange(0, len(mutatedGenes))
    newGene, alternate   = random.sample(geneSet, 2)
    mutatedGenes[index]  = alternate if newGene == mutatedGenes[index] else newGene
    return mutatedGenes


def mutate_chromosome(target:      Sequence,
                      geneSet:     Sequence,
                      parent:      Chromosome,
                      get_fitness: Callable
                      )->Chromosome:
    """Generate a mutated chromosome"""
    mutatedGenes = mutate_genes(parent.genes, geneSet)
    fitness      = get_fitness(mutatedGenes, target)
    return Chromosome(mutatedGenes, fitness)


def compare_with_target(target: str, guess: Chromosome)->bool:
    return guess.fitness == len(target)
