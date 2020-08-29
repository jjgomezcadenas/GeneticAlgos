# File: helloWorld.py

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
import urllib.request
import random
import datetime
from typing              import List, Dict, Tuple, Sequence, Callable
from networkx            import Graph
from matplotlib.patches  import Polygon
from shapely.geometry    import shape, MultiPolygon, LineString, MultiLineString

#1st stock
def load_map_data(file='africa.json'):
    """Loads json map data file"""

    with open(file) as f:
        data = json.load(f)
    return data


def view_map_data(data, ic=1):
    """Displays the structure of the map data file"""

    features = data['features']
    nb_countries = len(features)

    print(f'number of countries in map = {nb_countries}')

    print(f'view data for = {ic} countries')

    for idx in range(ic):
        props = features[idx]['properties']
        geom = features[idx]['geometry']
        country_geo = shape(geom)
        print(f'country number = {idx}')
        print(f'country properties = {props}')
        print(f'country geometry represented by {country_geo}')


#2nd stock
def build_gmap(jmap, mapName: str ='Africa Map', imax : int=0)->Graph:
    """Takes a jmap and returns a gMap (an object of type graph) representing the map including
    network information
    """

    def adjacency_test(country_geo1 : Polygon, country_geo2 : Polygon)->bool:
        """Returns True if the two countries are adjacent. Takes adavantage of
        the properties of Polygons (shape library objects), which "know" if they
        intersect.

        """
        return not country_geo1.intersection(country_geo2).is_empty

    def build_pols():
        """The geometrical object representing the geometry can be
        Polygons or a collection of Polygons (MultiPolygon). To pass the information to
        matplotlib we need a list of polygons. This function fills the dictionary
        name_pols with a list of polygons representing the country

        """
        if country_geo.geom_type == "MultiPolygon":
            polygons       = list(country_geo)
        elif country_geo.geom_type == "Polygon":
            polygons = [country_geo]
        else:
            print(f'found unexpected type, geom = {country_geo.geom_type}')

        name_pols[idx] = polygons

    def build_graph():
        """Builds a graph from the adjacency matrix and adds properties """

        G = nx.Graph(np.array(admat))
        G.graph['name'] = mapName

        print(f'built map graph, len = {len(G)}')

        for i in G.nodes:
            G.nodes[i]['name'] =name_map[i]
            G.nodes[i]['pols'] = name_pols[i]

        return G


    features     = jmap['features']
    nb_countries = len(features)
    name_map     = {}
    name_pols    = {}
    amat         = []

    print(f'number of countries in map = {nb_countries}')

    for idx in range(nb_countries):
        country_name = features[idx]['properties']['name']
        name_map[idx] = country_name
        geom = features[idx]['geometry']
        country_geo = shape(geom)

        if idx < imax:
            print(f' idx = {idx}, country = {country_name}, shape = {country_geo.geom_type}')

        build_pols()

        lst = []
        for oidx in range(nb_countries):
            other_name = features[oidx]['properties']['name']
            geom = features[oidx]['geometry']
            other_geo = shape(geom)

            if oidx < imax:
                print(f' oidx = {oidx}, country = {other_name}, shape = {other_geo.geom_type}')
                print(f'adjacency test = {adjacency_test(country_geo, other_geo) and country_name != other_name}')

            if adjacency_test(country_geo, other_geo) and country_name != other_name:
                lst.append(1)
            else:
                lst.append(0)

        amat.append(lst)

    admat = np.array(amat)
    print(f'built adjancency matrix, shape = {admat.shape}')

    return build_graph()

#3rd stock
def plot_gmap_monocolor(gMap : Graph, facecolor = 'gray', figsize=(30, 15)):
    """We use matplotlib to plot the collection of polygons in the map. We choose gray as color"""

    fig, ax = plt.subplots(figsize=figsize)

    POLS = list(gMap.nodes(data="pols")) # this provides [(0, lpol), (1, lpol)...]
    for lpol in POLS:
        for polygon in lpol[1]: # (0, pol) --> (0, list-of-polygons)
            mpl_poly = Polygon(np.array(polygon.exterior), facecolor=facecolor,
                               linewidth=5.0, alpha=0.5, edgecolor='black')
            ax.add_patch(mpl_poly)
    ax.relim()
    ax.autoscale()
    ax.axis('off')
    #return fig

#4th stock
def add_colors_to_gmap(gMap : Graph, colors : List):
    """Add a list of colors (one per node) to the gMap """
    for i in gMap.nodes:
        gMap.nodes[i]['color'] = COLORS[colors[i]]


def generate_parent_genes(length: int, geneSet: Sequence):
    """This function generates a list of genes (with length = length) from a gene set"""
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    return genes

#5th stock
def plot_gmap_color(wMap : Graph,figsize=(30, 15)):
    """Plot a color map using matplotlib. If not color is found use gray"""

    fig, ax = plt.subplots(figsize=figsize)

    POLS = list(wMap.nodes(data="pols"))
    cols = list(wMap.nodes(data="color"))
    for i, lpol in enumerate(POLS):
        for polygon in lpol[1]:
            col = cols[i][1]
            if col == None:
                facecolor = 'gray'
            else:
                facecolor = col

            mpl_poly = Polygon(np.array(polygon.exterior),
                               facecolor=facecolor,
                               linewidth=5.0, alpha=0.5, edgecolor='black')
            ax.add_patch(mpl_poly)
    ax.relim()
    ax.autoscale()
    ax.axis('off')

#5th stock
def mutate_genes(genes: List, geneSet: List):
    """Mutate genes, choosing a new gene from geneSet"""

    mutatedGenes         = genes[:]
    index                = random.randrange(0, len(mutatedGenes))
    newGene, alternate   = random.sample(geneSet, 2)
    mutatedGenes[index]  = alternate if newGene == mutatedGenes[index] else newGene
    return mutatedGenes


def fitness(gMap: Graph, imax=0):
    """Fitness function:
    1. For each node in map it finds all the edges
    2. Compares the color of the node with the color of each node pointed by the edge
    3. Increases by one unit if the colors are not the same

    """
    ft = 0
    for i in gMap.nodes:
        edges = gMap.edges([i]) # This returns [(i, j1), (i, j2)...] where (j1, j2) are the neighbours
        if i < imax:
            print(f"node = {i}, country = {gMap.nodes[i]['name']}, color = {gMap.nodes[i]['color']}")
            print(f"edges = {edges}")

        for e in edges:
            j = e[1] # index of neighbour
            if gMap.nodes[i]['color'] != gMap.nodes[j]['color']:
                ft+=1

            if i < imax:
                print(f"node = {j}, country = {gMap.nodes[j]['name']}, color = {gMap.nodes[j]['color']}")
                print(f"fitness = {ft}")


    return ft

#6th stock
def optimize(gMap : Graph, geneSet : List, get_fitness : Callable, optimalFitness : float,
             verbose=True, imax=10000):
    """The optimize function:
    1. Starts with a random gene sequence from the gene Set
    2. keeps mutating genes until optimal fitness is achieved
    """

    random.seed()
    startTime = datetime.datetime.now()
    guess = generate_parent_genes(len(gMap), geneSet)
    add_colors_to_gmap(gMap, guess)

    print(f'First guess = {guess}')

    i = 0
    ifmax = 0
    if verbose:
        ifmax = 10

    f = get_fitness(gMap, ifmax)

    ifmax = 0
    while f < optimalFitness and i < imax:
        newGuess = mutate_genes(guess, geneSet)
        add_colors_to_gmap(gMap, newGuess)
        fn = get_fitness(gMap, ifmax)
        time = datetime.datetime.now() - startTime
        if fn >= f:
            if verbose and fn > f:
                print(f'new guess increased fitness: {newGuess}, fitness = {fn} i = {i}, time = {time}')
            guess = newGuess
            f = fn

        i+=1
    return i, time, f, gMap



if __name__ == "__main__":
    colset = range(4) # five colors
    COLORS = {
        0: 'black',
        1: 'blue',
        2: 'green',
        3: 'yellow',
        #4: 'orange',
        }
    jmap_name = '../NB/africa.json'
    print(f'loading {jmap_name} map')
    jmap = load_map_data(file=jmap_name)

    wMap = build_gmap(jmap, mapName='Africa Map', imax =0)
    optimalFitness = len(wMap.edges) * 2
    print(f'optimalFitness = {optimalFitness}')

    #print(f'viewing {jmap_name} map')
    #view_map_data(jmap, ic=2)

    plot_gmap_monocolor(wMap, facecolor = 'green', figsize=(30, 15))
    plt.show()

    colors = generate_parent_genes(len(wMap), colset)
    cols =[COLORS[i] for i in colors]
    print(f'generate a list of {len(colors)} colors = {cols}')
    add_colors_to_gmap(wMap, colors)

    plot_gmap_color(wMap,figsize=(30, 15))
    plt.show()

    ft = fitness(wMap, imax=10)
    print(f'fitness = {ft}')
    colors2 = mutate_genes(colors, colset)
    add_colors_to_gmap(wMap, colors2)
    ft = fitness(wMap, imax=0)
    print(f'fitness = {ft}')

    i, time, ft, gMap = optimize(wMap, colset, fitness, optimalFitness, verbose=False, imax=10000)
    print(i)
    print(ft)
    print(optimalFitness)

    plot_gmap_color(gMap,figsize=(20, 20))
    plt.show()

    fig, ax = plt.subplots(figsize=(15,15))
    nx.draw(gMap, with_labels=True)
    plt.show()
