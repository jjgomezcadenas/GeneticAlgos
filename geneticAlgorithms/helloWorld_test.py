from pytest import fixture

from . genetic import Chromosome
from . genetic import string_to_list, list_to_string
from . genetic import mutate_chromosome
from . genetic import mutate_genes
from . genetic import generate_parent
from . genetic import compare_with_target

from . helloWorld import matching_string_fitness as get_fitness

@fixture(scope="session")
def geneSet():
    return " 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."


@fixture(scope="session")
def target():
    return "Hello Wonderful World!!!"

def test_chromosome(geneSet):
    c = Chromosome(string_to_list(geneSet), sum(1 for x in geneSet))
    assert list_to_string(c.genes) == geneSet and c.fitness == len(geneSet)


def test_get_fitness_target_equals_len(target):
    f = get_fitness(target, target)
    assert f == len(target)


def test_get_fitness_target_one_mutation(target, geneSet):
    mutatedTarget =mutate_genes(string_to_list(target), geneSet)
    f = get_fitness(mutatedTarget, target)
    assert f == len(target) -1


def test_generate_parent_yields_fitness_less_than_target_len(target, geneSet):
    c = generate_parent(target, geneSet, get_fitness)
    assert c.fitness < len(target)


def test_generate_parent_yields_correct_fitness(target, geneSet):
    c = generate_parent(target, geneSet, get_fitness)
    f = get_fitness(c.genes, target)

    assert c.fitness == f


def test_generate_parent_yields_correct_len(target, geneSet):
    c = generate_parent(target, geneSet, get_fitness)
    assert len(c.genes) == len(target)


def test_mutate_genes_gives_different_gene_sets(target, geneSet):
    guess = generate_parent(target, geneSet, get_fitness)
    mutatedGenes = mutate_genes(guess.genes, geneSet)
    assert mutatedGenes != guess.genes
