from pytest import fixture

from . genetic import Chromosome
from . genetic import string_to_list, list_to_string
from . genetic import mutate_chromosome
from . genetic import mutate_genes
from . genetic import generate_parent
from . genetic import compare_with_target

from . helloWorld import matching_string_fitness as get_fitness
from . helloWorld import guess_target


@fixture(scope="session")
def geneSets():
    return [" 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.",
            "01",[0,1],"012",[0,1,2],"1xyzm"]


@fixture(scope="session")
def targets():
    return ["Hello Wonderful World!!!", 10*["1"],20*[1], 10*['1'],10*[1],10*['1']]

def test_chromosome(geneSets):
    for geneSet in geneSets:
        c = Chromosome(string_to_list(geneSet), sum(1 for x in geneSet))
        assert list_to_string(c.genes) == list_to_string(geneSet)
        assert c.fitness == len(geneSet)


def test_get_fitness_target_equals_len(targets):
    for target in targets:
        f = get_fitness(target, target)
        assert f == len(target)


def test_get_fitness_target_one_mutation(targets, geneSets):
    for target, geneSet in zip(targets,geneSets):
        mutatedTarget =mutate_genes(string_to_list(target), geneSet)
        f = get_fitness(mutatedTarget, target)
        assert f == len(target) -1


def test_generate_parent_yields_fitness_less_than_target_len(targets, geneSets):
    for target, geneSet in zip(targets,geneSets):
        c = generate_parent(target, geneSet, get_fitness)
        assert c.fitness < len(target)


def test_generate_parent_yields_correct_fitness(targets, geneSets):
    for target, geneSet in zip(targets,geneSets):
        c = generate_parent(target, geneSet, get_fitness)
        f = get_fitness(c.genes, target)
        assert c.fitness == f


def test_generate_parent_yields_correct_len(targets, geneSets):
    for target, geneSet in zip(targets,geneSets):
        c = generate_parent(target, geneSet, get_fitness)
        assert len(c.genes) == len(target)


def test_mutate_genes_gives_different_gene_sets(targets, geneSets):
    for target, geneSet in zip(targets,geneSets):
        guess = generate_parent(target, geneSet, get_fitness)
        mutatedGenes = mutate_genes(guess.genes, geneSet)
        assert mutatedGenes != guess.genes


def test_hello_world(targets, geneSets):
    for target, geneSet in zip(targets,geneSets):
        i, time, guess = guess_target(target, geneSet)
        print(geneSet)
        print(target)
        print(guess.genes)
        assert list_to_string(guess.genes) == list_to_string(target)
