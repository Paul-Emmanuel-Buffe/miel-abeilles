import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import os


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


def plot_genealogy(parent_history, best_chemin_id, n_generations):
    """Affiche un arbre généalogique simplifié (ancienne version)"""
    plt.figure(figsize=(12, 6))
    generation_to_plot = min(n_generations - 1, len(parent_history))

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


def plot_genealogy_tree(tree, bee_id):
    """Affiche l'arbre généalogique complet d'une abeille"""
    
    # 1. Récupérer les données
    bee_info = tree.get_bee_info(bee_id)
    if not bee_info:
        print(f"Abeille {bee_id} introuvable")
        return
    
    ancestors = tree.get_ancestors(bee_id)
    niveaux = tree.organize_by_level(ancestors)
    positions = tree.calculate_positions(niveaux)
    
    # 2. Créer la figure
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('#F8F9FA')
    ax.axis('off')
    ax.set_aspect('equal')
    
    # 3. Dessiner les lignes parent → enfant
    for bee_id_key, info in ancestors.items():
        if bee_id_key not in positions:
            continue
            
        x1, y1 = positions[bee_id_key]
        
        # Parent 1 (ligne bleue)
        if pd.notna(info['parent_1']):
            parent_id = int(info['parent_1'])
            if parent_id in positions:
                x2, y2 = positions[parent_id]
                ax.plot([x1, x2], [y1, y2], color='#2E86AB', lw=2, alpha=0.7, zorder=1)
        
        # Parent 2 (ligne violette)
        if pd.notna(info['parent_2']):
            parent_id = int(info['parent_2'])
            if parent_id in positions:
                x2, y2 = positions[parent_id]
                ax.plot([x1, x2], [y1, y2], color='#A23B72', lw=2, alpha=0.7, zorder=1)
    
    # 4. Dessiner les rectangles (abeilles)
    for bee_id_key, (x, y) in positions.items():
        est_selectionnee = (bee_id_key == bee_id)
        
        if est_selectionnee:
            couleur, bordure, texte = '#F18F01', '#C73E1D', '#2C3E50'
            taille = 1.2
        else:
            couleur, bordure, texte = '#2E86AB', '#1B5E7D', '#F8F9FA'
            taille = 1.0
        
        largeur, hauteur = 0.6 * taille, 0.2 * taille
        
        # Fond blanc (cache les lignes)
        fond = FancyBboxPatch((x - largeur/2, y - hauteur/2), largeur, hauteur,
                              boxstyle="round,pad=0.03", facecolor='white',
                              edgecolor='white', zorder=10)
        ax.add_patch(fond)
        
        # Rectangle coloré
        rect = FancyBboxPatch((x - largeur/2, y - hauteur/2), largeur, hauteur,
                              boxstyle="round,pad=0.03", facecolor=couleur,
                              edgecolor=bordure, linewidth=2, zorder=11)
        ax.add_patch(rect)
        
        # Texte (ID de l'abeille)
        ax.text(x, y, f'{bee_id_key}', ha='center', va='center',
                fontweight='bold', color=texte, fontsize=7, zorder=12)
    
    # 5. Ajuster les limites
    all_x = [x for x, y in positions.values()]
    all_y = [y for x, y in positions.values()]
    if all_x and all_y:
        ax.set_xlim(min(all_x)-1.5, max(all_x)+1.5)
        ax.set_ylim(min(all_y)-1, max(all_y)+1)
    
    # 6. Titre et légende
    plt.title(f'Arbre Généalogique - Abeille {bee_id}\n'
              f'Distance: {bee_info["distance"]:.2f} • '
              f'Génération: {bee_info["generation"]}',
              fontsize=16, fontweight='bold', color='#2C3E50', pad=20)
    
    legende = [
        mpatches.Patch(facecolor='#F18F01', edgecolor='#C73E1D', 
                       label=f'Abeille {bee_id}'),
        mpatches.Patch(facecolor='#2E86AB', alpha=0.9, label='Lien parent 1'),
        mpatches.Patch(facecolor='#A23B72', alpha=0.9, label='Lien parent 2')
    ]
    ax.legend(handles=legende, loc='lower center', 
              bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=11)
    
    # Info nombre d'ancêtres
    ax.text(0.5, -0.12, f'{len(ancestors)} ancêtres • {len(niveaux)} niveaux',
            transform=ax.transAxes, ha='center', fontsize=10, 
            color='#7F8C8D', style='italic')
    
    plt.tight_layout()
    plt.show()


def explore_genealogy_interactive():
    """Mode interactif pour explorer les arbres généalogiques"""
    from genealogy import GenealogyTree
    
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
            plot_genealogy_tree(tree, bee_id)
            
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide")
        except Exception as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    explore_genealogy_interactive()