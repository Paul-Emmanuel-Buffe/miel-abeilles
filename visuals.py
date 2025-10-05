import os                # pour vérifier l'existence du fichier CSV
import pandas as pd      
import matplotlib.pyplot as plt  
from collections import defaultdict  # pour organiser les abeilles par génération
from genealogy import GenealogyTree

def plot_best_path(fleurs, best_chemin):
    """Affiche le meilleur parcours trouvé par l'algorithme génétique"""
    plt.figure(figsize=(8, 8))
    x = [fleurs[idx][0] for idx in best_chemin]
    y = [fleurs[idx][1] for idx in best_chemin]
    plt.plot(x, y, '-o', color='blue', markersize=5)
    plt.scatter(fleurs[0, 0], fleurs[0, 1], color='red', s=100, label='Ruche')
    plt.title("Meilleur parcours de l'abeille")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


def plot_avg_distance(avg_distances, n_generations):
    """Affiche l'évolution de la distance moyenne par génération"""
    plt.figure(figsize=(10, 5))
    plt.plot(range(n_generations), avg_distances, '-o', color='green')
    plt.xlabel("Génération")
    plt.ylabel("Distance moyenne")
    plt.title("Évolution du parcours moyen par génération")
    plt.grid(True)
    plt.show()


def plot_classic_tree(tree, bee_id):
     # Récupérer les ancêtres
    ancestors = tree.get_ancestors(bee_id)
    if not ancestors:
        print(f"Abeille {bee_id} introuvable")
        return
    
    # Organiser les abeilles par génération
    levels = defaultdict(list)
    for b_id, info in ancestors.items():
        levels[info['generation']].append(b_id)
    
    # Calculer positions simples : x centré par génération
    positions = {}
    for level, bees in levels.items():
        nb = len(bees)
        for i, b_id in enumerate(sorted(bees)):
            x = i - nb / 2  # centrer horizontalement
            y = -level       # génération 0 en haut
            positions[b_id] = (x, y)
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Tracer les liens parent → enfant
    for b_id, info in ancestors.items():
        x_child, y_child = positions[b_id]
        for parent_col in ['parent_1', 'parent_2']:
            if pd.notna(info[parent_col]):
                parent_id = int(info[parent_col])
                if parent_id in positions:
                    x_parent, y_parent = positions[parent_id]
                    ax.plot([x_child, x_parent], [y_child, y_parent],
                            color='gray', lw=1)
    
    # Tracer les nœuds
    for b_id, (x, y) in positions.items():
        if b_id == bee_id:
            ax.scatter(x, y, s=200, color='orange', zorder=5)
        else:
            ax.scatter(x, y, s=100, color='skyblue', zorder=5)
        ax.text(x, y, str(b_id), ha='center', va='center', fontsize=8, zorder=6)
    
    # Afficher
    plt.title(f"Arbre généalogique classique - Abeille {bee_id}", fontsize=14)
    plt.show()


def explore_genealogy_interactive():
    # Mode interactif pour explorer les arbres généalogiques
    if not os.path.exists('bees_log.csv'):
        print("Erreur: Fichier bees_log.csv non trouvé")
        return
    
    tree = GenealogyTree('bees_log.csv')
    df = tree.df
    
    print("\n" + "="*50)
    print("MODE INTERACTIF - Arbre généalogique")
    print("="*50)
    print(f"IDs disponibles : {df['id'].min()} à {df['id'].max()}")
    print(f"Générations : {df['generation'].min()} à {df['generation'].max()}")
    print("Tapez 'q' pour quitter\n")
    
    while True:
        user_input = input("Entrez l'ID de l'abeille : ").strip()
        
        if user_input.lower() == 'q':
            print("Au revoir !")
            break
        
        try:
            bee_id = int(user_input)
            
            if bee_id not in df['id'].values:
                print(f"Erreur: ID {bee_id} non trouvé")
                continue
            
            print(f"Génération de l'arbre pour l'abeille {bee_id}...")
            plot_classic_tree(tree, bee_id)
            
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide")
        except Exception as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    explore_genealogy_interactive()
