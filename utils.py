import numpy as np
import random

def chemin_aleatoire(fleurs, ruche=0):
    non_visitees = list(range(1, len(fleurs)))
    chemin = [ruche]
    while non_visitees:
        next_idx = random.choice(non_visitees)
        chemin.append(next_idx)
        non_visitees.remove(next_idx)
    chemin.append(ruche)
    return chemin

def distance_totale(chemin, fleurs):
    distance = 0
    x_prev, y_prev = fleurs[chemin[0]]
    for idx in chemin[1:]:
        x, y = fleurs[idx]
        distance += np.sqrt((x - x_prev)**2 + (y - y_prev)**2)
        x_prev, y_prev = x, y
    return distance

def mutation(chemin, mutation_rate):
    genome_mut = chemin.copy()
    if np.random.rand() < mutation_rate:
        i, j = np.random.choice(range(1, len(genome_mut)-1), 2, replace=False)
        genome_mut[i], genome_mut[j] = genome_mut[j], genome_mut[i]
    return genome_mut
