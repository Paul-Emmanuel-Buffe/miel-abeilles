import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd


from selection_rules import create_child
from utils import chemin_aleatoire, distance_totale, mutation
from visuals import plot_best_path, plot_avg_distance, plot_genealogy
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
n_generations = 50
mutation_rate = 0.20
elitisme_rates = [0.2]

# ----------------------
# Génération initiale
# ----------------------
population = [chemin_aleatoire(fleurs, ruche) for _ in range(n_abeilles)]
all_nodes = list(range(len(fleurs)))

# Pour stocker l’évolution des distances moyennes et les parents
avg_distances = []
parent_history = []  # Liste de tuples (parents, enfants) par génération

## ----------------------
# Boucle évolution
# ----------------------
bee_counter = MrBee() # Initialisation de l'objet de comptage
simulation_id = 1     # Renseigner l'id de la simulation

for generation in range(n_generations):
    distances = [distance_totale(chemin, fleurs) for chemin in population]
    avg_distances.append(np.mean(distances))

    rate = elitisme_rates[min(generation, len(elitisme_rates)-1)]
    n_parents = max(2, int(rate * n_abeilles))
    sorted_indices = np.argsort(distances)
    parents = [population[i] for i in sorted_indices[:n_parents]]

    # Calculer le taux d'élitisme de cette génération
    current_elitisme_rate = elitisme_rates[min(generation, len(elitisme_rates)-1)]

    enfants = []
    gen_parents_children = []  # stocke les relations parent->enfant
    
    for _ in range(n_abeilles - n_parents):
        p1, p2 = random.sample(parents, 2)
        child = create_child(p1, p2, all_nodes, hive=ruche)
        child = mutation(child, mutation_rate)
        enfants.append(child)
        gen_parents_children.append((p1, p2, child))

        # Enregistrement transmis à MrBee() - pour chaque enfant créé
        bee_counter.add_bee(
            simulation_id=simulation_id,
            generation=generation,
            distance=distance_totale(child, fleurs),
            parent_1=p1,
            parent_2=p2,
            chemin=child,
            n_generations=n_generations,
            mutation_rate=mutation_rate,
            elitisme_rate=current_elitisme_rate
        )

    parent_history.append(gen_parents_children)
    population = parents + enfants
# ----------------------
# Résultat final
# ----------------------
distances = [distance_totale(chemin, fleurs) for chemin in population]
best_idx = np.argmin(distances)
best_chemin = population[best_idx]
print("Meilleur parcours :", best_chemin)
print("Distance :", distances[best_idx])

plot_best_path(fleurs, best_chemin)
plot_avg_distance(avg_distances, n_generations)
plot_genealogy(parent_history, best_chemin, n_generations)

# Enregistrement de TOUTES les abeilles de la simulation effectuée
bee_counter.save_csv("bees_log.csv")

# +++++++ A suprimer => visualistion des données ++++


# Charger le CSV
df = pd.read_csv("bees_log.csv")

# Affichage 
print("\n=== Aperçu des 5 premières abeilles ===\n")
print(df.head())  
print("\n======================================\n")
