import numpy as np
import random
import matplotlib.pyplot as plt
from selection_rules import create_child
from utils import chemin_aleatoire, distance_totale, mutation


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
n_generations = 500
mutation_rate = 0.1
elitisme_rates = [0.5, 0.4, 0.3, 0.2]

# ----------------------
# Génération initiale
# ----------------------
population = [chemin_aleatoire(fleurs, ruche) for _ in range(n_abeilles)]
all_nodes = list(range(len(fleurs)))

# Pour stocker l’évolution des distances moyennes et les parents
avg_distances = []
parent_history = []  # Liste de tuples (parents, enfants) par génération

# ----------------------
# Boucle évolution
# ----------------------
for generation in range(n_generations):
    distances = [distance_totale(chemin, fleurs) for chemin in population]
    avg_distances.append(np.mean(distances))

    rate = elitisme_rates[min(generation, len(elitisme_rates)-1)]
    n_parents = max(2, int(rate * n_abeilles))
    sorted_indices = np.argsort(distances)
    parents = [population[i] for i in sorted_indices[:n_parents]]

    enfants = []
    gen_parents_children = []  # stocke les relations parent->enfant
    for _ in range(n_abeilles - n_parents):
        p1, p2 = random.sample(parents, 2)
        child = create_child(p1, p2, all_nodes, hive=ruche)
        child = mutation(child, mutation_rate)
        enfants.append(child)
        gen_parents_children.append((p1, p2, child))
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

# ----------------------
# 1️⃣ Graphique du meilleur parcours
# ----------------------
plt.figure(figsize=(8,8))
x = [fleurs[idx][0] for idx in best_chemin]
y = [fleurs[idx][1] for idx in best_chemin]
plt.plot(x, y, '-o', color='blue', markersize=5)
plt.scatter(fleurs[0,0], fleurs[0,1], color='red', s=100, label='Ruche')
plt.title("Meilleur parcours de l'abeille")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()

# ----------------------
# 2️⃣ Evolution du temps de parcours moyen
# ----------------------
plt.figure(figsize=(10,5))
plt.plot(range(n_generations), avg_distances, '-o', color='green')
plt.xlabel("Génération")
plt.ylabel("Distance moyenne")
plt.title("Évolution du parcours moyen par génération")
plt.grid(True)
plt.show()

# ----------------------
# 3️⃣ Visualisation simplifiée de l'arbre généalogique
# ----------------------
# On ne fait pas un arbre complet mais une visualisation parent->enfant du meilleur chemin
plt.figure(figsize=(12,6))
generation_to_plot = min(10, n_generations)  # ne pas surcharger
y_offset = 0
for gen in range(generation_to_plot):
    for p1, p2, child in parent_history[gen]:
        if child == best_chemin:  # ne tracer que les liens menant au meilleur chemin
            plt.plot([gen, gen+1], [y_offset, y_offset+1], 'ro-')
            y_offset += 1
plt.xlabel("Générations")
plt.ylabel("Chemins menant au meilleur parcours")
plt.title("Arbre généalogique simplifié du meilleur parcours")
plt.show()