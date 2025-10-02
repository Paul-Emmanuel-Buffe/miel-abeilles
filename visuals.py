import matplotlib.pyplot as plt

def plot_best_path(fleurs, best_chemin):
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

def plot_avg_distance(avg_distances, n_generations):
    plt.figure(figsize=(10,5))
    plt.plot(range(n_generations), avg_distances, '-o', color='green')
    plt.xlabel("Génération")
    plt.ylabel("Distance moyenne")
    plt.title("Évolution du parcours moyen par génération")
    plt.grid(True)
    plt.show()

def plot_genealogy(parent_history, best_chemin_id, n_generations):
    plt.figure(figsize=(12, 6))
    generation_to_plot = min(n_generations - 1, len(parent_history))  # On commence à la génération 1

    y_offset = 0
    for gen in range(generation_to_plot):
        if gen < len(parent_history):
            for p1, p2, child_id in parent_history[gen]:
                if child_id == best_chemin_id:
                    plt.plot([gen, gen + 1], [y_offset, y_offset + 1], 'ro-')
                    y_offset += 1

    plt.xlabel("Générations")
    plt.ylabel("Chemins menant au meilleur parcours")
    plt.title("Arbre généalogique simplifié du meilleur parcours")
    plt.show()
