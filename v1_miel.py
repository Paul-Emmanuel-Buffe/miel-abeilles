import matplotlib.pyplot as plt
import numpy as np
import random

# Coordonnées des fleurs
fleurs = np.array([
    [796,310],[774,130],[116,69],[908,534],[708,99],[444,428],[220,307],[501,287],[345,560],[628,311],
    [901,639],[436,619],[938,646],[45,549],[837,787],[328,489],[278,434],[704,995],[101,482],[921,964],
    [493,970],[494,898],[929,389],[730,742],[528,794],[371,429],[98,711],[724,631],[573,903],[964,726],
    [213,639],[549,329],[684,273],[273,105],[897,324],[508,31],[758,405],[862,361],[898,898],[2,897],
    [951,209],[189,739],[602,68],[437,601],[330,410],[3,517],[643,404],[875,407],[761,772],[276,666]
])

# Position de la ruche
ruche = np.array([500, 500])

# Paramètres
n_abeilles = 100
n_generations = 50
mutation_rate = 0.1

# Fonction pour générer un chemin aléatoire DFS-like
def chemin_aleatoire(fleurs, ruche):
    non_visitees = list(range(len(fleurs)))
    chemin = []
    while non_visitees:
        next_idx = np.random.choice(non_visitees)
        chemin.append(next_idx)
        non_visitees.remove(next_idx)
    return chemin

# Générer la population
population = []
for _ in range(n_abeilles):
    chemin = chemin_aleatoire(fleurs, ruche)
    population.append(chemin)


# Afficher tous les chemins
for i, chemin in enumerate(population):
    print(f"Abeille {i+1}: {chemin}")
    #print(f"Abeille {i+1}: {chemin} {len(chemin)}")

# Fonction pour calculer la distance totale d'un parcours
def distance_totale(chemin, fleurs, ruche):
    distance=0
    x_dep, y_dep = ruche #point de départ à la ruche en (500,500)
    for idx in chemin:
        x,y = fleurs[idx]
        distance += np.sqrt((x-x_dep)**2+(y-y_dep)**2)#distance euclidienne
        x_dep, y_dep = x,y
    distance += np.sqrt((ruche[0] - x_dep)**2 + (ruche[1] - y_dep)**2)
    return distance

# Test du calcul sur une abeille
abeille_0=population[0]
print(distance_totale(abeille_0, fleurs, ruche))

#Mutation : swap vu en How To - à revoir
def mutation(chemin, mutation_rate):
    genome_mut = chemin.copy()
    if np.random.rand<mutation_rate:
        i, j = np.random.choice(len(genome_mut), 2, replace=False)
        genome_mut[i], genome_mut[j] = genome_mut[j], genome_mut[i]
    return genome_mut

