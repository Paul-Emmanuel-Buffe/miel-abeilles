import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import os

from genealogy import GenealogyTree
from visuals import plot_best_path, plot_avg_distance, plot_classic_tree  # <-- nouveau nom
from selection_rules import create_child, create_child_order_crossover
from utils import chemin_aleatoire, distance_totale, mutation
from bee_count import MrBee

# ----------------------
# Coordonnées des fleurs + ruche
# ----------------------
ruche_coord = np.array([500, 500])
fleurs_fleurs = np.array([
    [796,310],[774,130],[116,69],[908,534],[708,99],[444,428],[220,307],[501,287],[345,560],[628,311],
    [901,639],[436,619],[938,646],[45,549],[837,787],[328,489],[278,434],[704,995],[101,482],[921,964],
    [493,970],[494,898],[929,389],[730,742],[528,794],[371,429],[98,711],[724,631],[573,903],[964,726],
    [213,639],[549,329],[684,273],[273,105],[897,324],[508,31],[758,405],[862,361],[898,898],[2,897],
    [951,209],[189,739],[602,68],[437,601],[330,410],[3,517],[643,404],[875,407],[761,772],[276,666]
])
fleurs = np.vstack([ruche_coord, fleurs_fleurs])  # La ruche devient l'indice 0

# ----------------------
# Paramètres
# ----------------------
ruche = 0
n_abeilles = 100
n_generations = 1300
mutation_rate = 0.20
elitisme_rates = [0.2]
crossover_method = "order_crossover"  # "common_edges" ou "order_crossover"

# ----------------------
# Génération initiale
# ----------------------
bee_counter = MrBee()
simulation_id = 1

population = []
for i in range(n_abeilles):
    chemin = chemin_aleatoire(fleurs, ruche)
    bee_id = bee_counter.add_bee(
        simulation_id=simulation_id,
        generation=0,
        distance=distance_totale(chemin, fleurs),
        parent_1=None,
        parent_2=None,
        chemin=chemin,
        n_generations=n_generations,
        mutation_rate=mutation_rate,
        elitisme_rate=elitisme_rates[0],
        crossover_method=crossover_method
    )
    population.append((bee_id, chemin))

all_nodes = list(range(len(fleurs)))

# Pour stocker l'évolution des distances moyennes et les parents
avg_distances = []
parent_history = []

# ----------------------
# Boucle évolution
# ----------------------
for generation in range(n_generations):
    distances = [distance_totale(chemin, fleurs) for (_, chemin) in population]
    avg_distances.append(np.mean(distances))

    rate = elitisme_rates[min(generation, len(elitisme_rates)-1)]
    n_parents = max(2, int(rate * n_abeilles))
    sorted_indices = np.argsort(distances)
    parents = [population[i] for i in sorted_indices[:n_parents]]

    current_elitisme_rate = elitisme_rates[min(generation, len(elitisme_rates)-1)]

    enfants = []
    gen_parents_children = []

    for _ in range(n_abeilles - n_parents):
        (p1_id, p1), (p2_id, p2) = random.sample(parents, 2)

        if crossover_method == "common_edges":
            child = create_child(p1, p2, all_nodes, hive=ruche)
        elif crossover_method == "order_crossover":
            child = create_child_order_crossover(p1, p2, all_nodes, hive=ruche)
        else:
            raise ValueError("Méthode de croisement non reconnue")

        child = mutation(child, mutation_rate)

        child_id = bee_counter.add_bee(
            simulation_id=simulation_id,
            generation=generation + 1,
            distance=distance_totale(child, fleurs),
            parent_1=p1_id,
            parent_2=p2_id,
            chemin=child,
            n_generations=n_generations,
            mutation_rate=mutation_rate,
            elitisme_rate=current_elitisme_rate,
            crossover_method=crossover_method
        )
        enfants.append((child_id, child))
        gen_parents_children.append((p1_id, p2_id, child_id))

    parent_history.append(gen_parents_children)
    population = parents + enfants

# ----------------------
# Résultat final
# ----------------------
distances = [distance_totale(chemin, fleurs) for (_, chemin) in population]
best_idx = np.argmin(distances)
best_id, best_chemin = population[best_idx]

print("Meilleur parcours (id={}):".format(best_id), best_chemin)
print("Distance :", distances[best_idx])

# ----------------------
# Sauvegarde CSV
# ----------------------
bee_counter.save_csv("bees_log.csv")

# ----------------------
# Visualisation
# ----------------------
plot_best_path(fleurs, best_chemin)
plot_avg_distance(avg_distances, n_generations)

print(f"\n=== Génération de l'arbre généalogique de l'abeille {best_id} ===")
tree = GenealogyTree("bees_log.csv")
plot_classic_tree(tree, best_id)  
