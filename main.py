import ant_farm
import sys
import random
import numpy as np
from copy import deepcopy
import matplotlib
matplotlib.use('agg')

from matplotlib import pyplot as plt, rcParams, ticker, colors, colorbar

iterate = int(sys.argv[1])
ant_pop = int(sys.argv[2])
evaporation = float(sys.argv[3])
file_path = sys.argv[4]

'''Optional, to auto create all vertices'''
keys_num = (sys.argv[5])

alter = sys.argv[6]

if(keys_num == 'None'):
    farm = ant_farm.Graph()
else:
    keys_num = int(keys_num)
    farm = ant_farm.Graph(keys_num)


for line in open(file_path):
    vert, nei, weight = line.replace('\n', '').split()
    vert = int(vert)
    nei = int(nei)
    weight = int(weight)
    if vert not in farm.graph:
        farm.add_vert(vert)
    farm.add_edge((vert, nei, weight))

# Objeto do Ant Colony Optimazation
aco = ant_farm.Aco(farm.graph, evaporation)

top = []

g = 20 # Number of iterations

for seed in range(g):
    random.seed(seed)
    best_ants = []
    for iter in range(iterate):
        valid_ants = []

        for i in range(ant_pop):
            ant = ant_farm.Ant(iter, i, seed)
            aco.walk_ant(ant, valid_ants)

        aco.pherom_update(valid_ants)
        aco.best_ants(valid_ants, best_ants)

    best_ants = sorted(best_ants, key=lambda x: -x.peso)
    top.append(best_ants[0])

top_sorted = sorted(top, key=lambda x: x.peso)

plot_top = [i.peso for i in top]
gens = [i+1 for i in range(g)]

rcParams['figure.figsize'] = (18,15)
fig, (ax) = plt.subplots()

################################plos bests######################################
N = ax.plot(gens, plot_top, color='red', marker='o')

ax.set_title('Melhores Caminhos por iteração',size=12)
ax.set_ylabel('Valor do Caminho', size=12)
ax.set_xlabel("Iteração", size=12)

ax.grid(linestyle='--', linewidth=0.5)
major_ticks = gens
ax.set_xticks(major_ticks)

fig.savefig(alter, dpi=75)
