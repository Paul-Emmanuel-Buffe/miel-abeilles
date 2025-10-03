import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import pandas as pd


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


def plot_genealogy_tree(genealogy_tree, bee_id):
    """
    Affiche l'arbre généalogique complet d'une abeille
    
    Args:
        genealogy_tree: Instance de GenealogyTree
        bee_id (int): ID de l'abeille dont on veut voir l'arbre
    """
    # Vérifier que l'abeille existe
    bee_info = genealogy_tree.get_bee_info(bee_id)
    if bee_info is None:
        print(f"Erreur: Abeille {bee_id} non trouvée")
        return
    
    # Récupérer les données
    ancestors = genealogy_tree.get_ancestors(bee_id)
    
    if not ancestors:
        print("Aucun ancêtre trouvé")
        return
    
    generations = genealogy_tree.organize_by_generation(ancestors)
    positions = genealogy_tree.calculate_positions(generations)
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(18, 12))
    
    # Dessiner les lignes de parenté
    _draw_parent_lines(ax, ancestors, positions)
    
    # Dessiner les nœuds (abeilles)
    _draw_bee_nodes(ax, bee_id, positions)
    
    # Configuration du graphique
    _configure_genealogy_plot(ax, fig, bee_id, bee_info, positions, ancestors, generations)
    
    plt.tight_layout()
    plt.show()


def _draw_parent_lines(ax, ancestors, positions):
    """Dessine les lignes reliant les enfants à leurs parents"""
    for bee_id_key, info in ancestors.items():
        if bee_id_key in positions:
            x1, y1 = positions[bee_id_key]
            
            if pd.notna(info['parent_1']) and int(info['parent_1']) in positions:
                x2, y2 = positions[int(info['parent_1'])]
                ax.plot([x1, x2], [y1, y2], color='#2E86AB', linewidth=2.2, alpha=0.8)
            
            if pd.notna(info['parent_2']) and int(info['parent_2']) in positions:
                x2, y2 = positions[int(info['parent_2'])]
                ax.plot([x1, x2], [y1, y2], color='#A23B72', linewidth=2.2, alpha=0.8)


def _draw_bee_nodes(ax, selected_bee_id, positions):
    """Dessine les nœuds représentant chaque abeille"""
    for bee_id_key, (x, y) in positions.items():
        is_selected = bee_id_key == selected_bee_id
        
        # Couleurs selon si c'est l'abeille sélectionnée ou non
        if is_selected:
            color = '#F18F01'  # Orange
            edge_color = '#C73E1D'
            text_color = '#2C3E50'
            size_factor = 1.2
        else:
            color = '#2E86AB'  # Bleu
            edge_color = '#1B5E7D'
            text_color = '#F8F9FA'
            size_factor = 1.0
        
        # Nœud avec coins arrondis
        width, height = 0.6 * size_factor, 0.2 * size_factor
        
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                            boxstyle="round,pad=0.03",
                            facecolor=color, edgecolor=edge_color,
                            linewidth=2.0, alpha=0.95)
        ax.add_patch(box)
        
        # Texte centré
        ax.text(x, y, f'{bee_id_key}', ha='center', va='center', 
                fontweight='bold', color=text_color, fontsize=7)


def _configure_genealogy_plot(ax, fig, bee_id, bee_info, positions, ancestors, generations):
    """Configure l'apparence générale du graphique de généalogie"""
    # Limites du graphique
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    
    if all_x and all_y:
        ax.set_xlim(min(all_x)-1.5, max(all_x)+1.5)
        ax.set_ylim(min(all_y)-1, max(all_y)+1)
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Arrière-plan
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    
    # Titre avec clarification
    plt.title(f'Arbre Généalogique - Abeille {bee_id}\n'
              f'Distance: {bee_info["distance"]:.2f} • '
              f'Génération simulation: {bee_info["generation"]}', 
              fontsize=18, fontweight='bold', color='#2C3E50', pad=30)
    
    # Légende
    legend_elements = [
        mpatches.Patch(facecolor='#F18F01', edgecolor='#C73E1D', 
                       label=f'Abeille {bee_id}', linewidth=2),
        mpatches.Patch(facecolor='#2E86AB', alpha=0.9, label='Parent 1'),
        mpatches.Patch(facecolor='#A23B72', alpha=0.9, label='Parent 2')
    ]
    
    ax.legend(handles=legend_elements, loc='lower center', 
              bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=12,
              framealpha=0.95, edgecolor='#BDC3C7', 
              facecolor='white', fancybox=True, shadow=True)
    
    # Information en bas avec clarification
    ax.text(0.5, -0.15, f'{len(ancestors)} ancêtres • {len(generations)} niveaux généalogiques', 
            transform=ax.transAxes, ha='center', va='center',
            fontsize=10, color='#7F8C8D', style='italic',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))


def explore_genealogy_interactive():
    """
    Mode interactif pour explorer les arbres généalogiques
    """
    import os
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
    print(f"Générations simulation : {df['generation'].min()} à {df['generation'].max()}")
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
                print(f"Les IDs valides vont de {df['id'].min()} à {df['id'].max()}")
                continue
            
            print(f"Génération de l'arbre pour l'abeille {bee_id}...")
            plot_genealogy_tree(tree, bee_id)
            
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide ou 'q' pour quitter")
        except Exception as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    explore_genealogy_interactive()