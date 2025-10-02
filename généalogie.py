import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def load_bee_data(filepath):
    """Charge les données du fichier CSV"""
    return pd.read_csv(filepath)

def get_ancestors(df, bee_id, max_generations=10):
    """Récupère tous les ancêtres d'une abeille"""
    ancestors = {}
    
    def trace_parents(current_id, generation=0):
        if generation >= max_generations or current_id not in df['id'].values:
            return
        
        bee = df[df['id'] == current_id].iloc[0]
        ancestors[current_id] = {
            'generation': generation,
            'parent_1': bee['parent_1'],
            'parent_2': bee['parent_2'],
            'distance': bee['distance'],
            'simulation_id': bee['simulation_id']
        }
        
        # Récursivement tracer les parents
        if pd.notna(bee['parent_1']):
            trace_parents(int(bee['parent_1']), generation + 1)
        if pd.notna(bee['parent_2']):
            trace_parents(int(bee['parent_2']), generation + 1)
    
    trace_parents(bee_id)
    return ancestors

def plot_genealogy_tree(df, bee_id, max_generations=8):
    """Affiche l'arbre généalogique d'une abeille sans distances et sans étiquettes de génération"""
    
    # Vérifier que l'abeille existe
    if bee_id not in df['id'].values:
        print(f"Erreur: L'abeille avec l'ID {bee_id} n'existe pas dans les données.")
        return
    
    # Récupérer les ancêtres
    ancestors = get_ancestors(df, bee_id, max_generations)
    
    if not ancestors:
        print(f"Aucun ancêtre trouvé pour l'abeille {bee_id}")
        return
    
    # Organiser les abeilles par génération
    generations = {}
    for bee_id_key, info in ancestors.items():
        gen = info['generation']
        if gen not in generations:
            generations[gen] = []
        generations[gen].append(bee_id_key)
    
    # Créer la figure
    max_gen = max(generations.keys())
    fig_width = max(12, len(generations[0]) * 2)
    fig_height = max(8, (max_gen + 1) * 1.2)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Paramètres de disposition
    y_spacing = 1.5
    x_spacing = 2.0
    
    # Calculer les positions
    positions = {}
    
    for gen in sorted(generations.keys()):
        bees_in_gen = generations[gen]
        num_bees = len(bees_in_gen)
        y_pos = gen * y_spacing  # Génération 0 en bas
        
        # Centrer horizontalement chaque génération
        total_width = (num_bees - 1) * x_spacing
        start_x = -total_width / 2
        
        for i, bee_id_key in enumerate(bees_in_gen):
            x_pos = start_x + i * x_spacing
            positions[bee_id_key] = (x_pos, y_pos)
    
    # Dessiner les connexions (lignes entre parents et enfants)
    for bee_id_key, info in ancestors.items():
        if bee_id_key in positions:
            x1, y1 = positions[bee_id_key]
            
            # Connexion avec parent_1
            if pd.notna(info['parent_1']) and int(info['parent_1']) in positions:
                x2, y2 = positions[int(info['parent_1'])]
                ax.plot([x1, x2], [y1, y2], 'steelblue', linewidth=2, alpha=0.8, zorder=1)
            
            # Connexion avec parent_2
            if pd.notna(info['parent_2']) and int(info['parent_2']) in positions:
                x2, y2 = positions[int(info['parent_2'])]
                ax.plot([x1, x2], [y1, y2], 'coral', linewidth=2, alpha=0.8, zorder=1)
    
    # Dessiner les nœuds (abeilles) - SANS les distances
    for bee_id_key, (x, y) in positions.items():
        info = ancestors[bee_id_key]
        
        # Couleur selon la génération
        color = plt.cm.Blues(0.3 + info['generation'] / max(1, max_gen) * 0.6)
        
        # Style différent pour l'abeille sélectionnée
        is_selected = bee_id_key == bee_id
        
        # Taille du nœud (réduite car pas de texte de distance)
        width, height = 0.8, 0.3
        
        # Dessiner le rectangle pour l'abeille
        box_style = "round,pad=0.1" if is_selected else "round,pad=0.05"
        edge_width = 3 if is_selected else 1.5
        face_alpha = 0.9 if is_selected else 0.8
        
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                              boxstyle=box_style,
                              edgecolor='darkred' if is_selected else 'black', 
                              facecolor=color,
                              linewidth=edge_width,
                              alpha=face_alpha,
                              zorder=2)
        ax.add_patch(box)
        
        # Texte avec l'ID seulement (plus de distance)
        font_size_id = 9 if is_selected else 8
        ax.text(x, y, f'{bee_id_key}', 
                ha='center', va='center', fontsize=font_size_id, 
                fontweight='bold' if is_selected else 'normal', 
                color='white', zorder=3)
    
    # Configuration du graphique avec limites adaptatives
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]
    
    x_margin = 1.5
    y_margin = 0.8
    
    ax.set_xlim(min(all_x) - x_margin, max(all_x) + x_margin)
    ax.set_ylim(min(all_y) - y_margin, max(all_y) + y_margin)
    ax.set_aspect('equal')
    ax.axis('off')  # Désactive tous les axes et labels
    
    # Titre amélioré
    bee_info = df[df['id'] == bee_id].iloc[0]
    plt.title(f'Arbre généalogique de l\'abeille {bee_id}\n' + 
              f'Distance: {bee_info["distance"]:.2f} | ' +
              f'Génération: {bee_info["generation"]} | ' +
              f'Simulation: {bee_info["simulation_id"]}',
              fontsize=14, fontweight='bold', pad=20)
    
    # Légende placée en bas
    legend_elements = [
        mpatches.Patch(facecolor='darkred', edgecolor='darkred', alpha=0.9, 
                       label=f'Abeille sélectionnée (ID: {bee_id})'),
        mpatches.Patch(facecolor='steelblue', alpha=0.8, 
                       label='Ligne parent 1'),
        mpatches.Patch(facecolor='coral', alpha=0.8, 
                       label='Ligne parent 2')
    ]
    
    # Placer la légende en bas au centre
    legend = ax.legend(handles=legend_elements, loc='lower center', 
                      bbox_to_anchor=(0.5, -0.05),  # Position sous le graphique
                      ncol=3,  # 3 colonnes pour une disposition horizontale
                      framealpha=0.95,
                      fancybox=True, shadow=True, fontsize=10)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('gray')
    
    # Ajuster les marges pour faire de la place à la légende en bas
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

def print_genealogy_info(df, bee_id, max_generations=8):
    """Affiche des informations sur la généalogie en console"""
    ancestors = get_ancestors(df, bee_id, max_generations)
    
    if not ancestors:
        print(f"Aucun ancêtre trouvé pour l'abeille {bee_id}")
        return
    
    generations = {}
    for bee_id_key, info in ancestors.items():
        gen = info['generation']
        if gen not in generations:
            generations[gen] = []
        generations[gen].append(bee_id_key)
    
    print(f"\n=== INFORMATIONS GÉNÉALOGIQUES - Abeille {bee_id} ===")
    print(f"Nombre total d'ancêtres: {len(ancestors)}")
    print(f"Nombre de générations: {len(generations)}")
    
    for gen in sorted(generations.keys()):
        print(f"  Niveau {gen}: {len(generations[gen])} abeilles")

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données
    df = load_bee_data('bees_log.csv')
    
    # Afficher les informations en console
    bee_id = 800
    print_genealogy_info(df, bee_id, max_generations=6)
    
    # Afficher l'arbre généalogique sans distances et sans étiquettes
    plot_genealogy_tree(df, bee_id, max_generations=6)
    
    # Vous pouvez aussi essayer d'autres abeilles:
    # plot_genealogy_tree(df, 100, max_generations=5)
    # plot_genealogy_tree(df, 500, max_generations=6)