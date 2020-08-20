from pytest import fixture

from geneticAlgorithms.genetic_sort import Chromosome
from geneticAlgorithms.genetic_sort import Fitness
from geneticAlgorithms.genetic_sort import mutate_chromosome
from geneticAlgorithms.genetic_sort import generate_parent
from geneticAlgorithms.genetic_sort import get_fitness
from geneticAlgorithms.genetic_sort import compare_fitness

from geneticAlgorithms.Sort import sort_numbers


@fixture(scope="session")
def geneSet():
    return [i for i in range(100)]


def test_sort_numbers(geneSet):
    for lengthOfList in [5,10,20]:
        i, time, sorted = sort_numbers(lengthOfList, geneSet, verbose=True, imax=1000000)

        assert sorted.fitness.sortCount == lengthOfList
