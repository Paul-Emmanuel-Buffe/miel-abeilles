import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

def load_bee_data(filepath='bees_log.csv'):
    return pd.read_csv(filepath)

def get_ancestors(df, bee_id):
    ancestors = {}
    
    def trace_parents(current_id, generation=0):
        if current_id not in df['id'].values:
            return
        
        bee = df[df['id'] == current_id].iloc[0]
        ancestors[current_id] = {
            'generation': generation,
            'parent_1': bee['parent_1'],
            'parent_2': bee['parent_2']
        }
        
        if pd.notna(bee['parent_1']):
            trace_parents(int(bee['parent_1']), generation + 1)
        if pd.notna(bee['parent_2']):
            trace_parents(int(bee['parent_2']), generation + 1)
    
    trace_parents(bee_id)
    return ancestors

def plot_genealogy_tree(df, bee_id):
    if bee_id not in df['id'].values:
        print(f"Erreur: Abeille {bee_id} non trouvée")
        return
    
    ancestors = get_ancestors(df, bee_id)
    
    if not ancestors:
        print("Aucun ancêtre trouvé")
        return
    
    # Organiser par génération
    generations = {}
    for bee_id_key, info in ancestors.items():
        gen = info['generation']
        if gen not in generations:
            generations[gen] = []
        generations[gen].append(bee_id_key)
    
    # Calculer les positions
    positions = {}
    for gen in sorted(generations.keys()):
        bees = generations[gen]
        y = gen * 2.0
        total_width = (len(bees) - 1) * 2.5
        start_x = -total_width / 2
        
        for i, bee_id_key in enumerate(bees):
            x = start_x + i * 2.5
            positions[bee_id_key] = (x, y)
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(18, 12))
    
    # Dessiner les lignes
    for bee_id_key, info in ancestors.items():
        if bee_id_key in positions:
            x1, y1 = positions[bee_id_key]
            
            if pd.notna(info['parent_1']) and int(info['parent_1']) in positions:
                x2, y2 = positions[int(info['parent_1'])]
                ax.plot([x1, x2], [y1, y2], color='#2E86AB', linewidth=2.2, alpha=0.8)
            
            if pd.notna(info['parent_2']) and int(info['parent_2']) in positions:
                x2, y2 = positions[int(info['parent_2'])]
                ax.plot([x1, x2], [y1, y2], color='#A23B72', linewidth=2.2, alpha=0.8)
    
    # Dessiner les nœuds
    for bee_id_key, (x, y) in positions.items():
        is_selected = bee_id_key == bee_id
        
        # Palette de couleurs
        if is_selected:
            color = '#F18F01'  # Orange
            edge_color = '#C73E1D'
            text_color = '#2C3E50'  # Bleu foncé pour meilleur contraste
            size_factor = 1.2
        else:
            color = '#2E86AB'  # Bleu
            edge_color = '#1B5E7D'
            text_color = '#F8F9FA'  # Blanc cassé pour meilleur contraste
            size_factor = 1.0
        
        # Nœud avec coins arrondis - taille réduite
        width, height = 0.6 * size_factor, 0.2 * size_factor  # Réduit la taille
        
        # Utiliser FancyBboxPatch pour les coins arrondis
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                            boxstyle="round,pad=0.03",  # Padding réduit
                            facecolor=color, edgecolor=edge_color,
                            linewidth=2.0, alpha=0.95)
        ax.add_patch(box)
        
        # Texte centré - taille réduite
        ax.text(x, y, f'{bee_id_key}', ha='center', va='center', 
                fontweight='bold', color=text_color, fontsize=7)  # Taille réduite à 7
    
    # Configuration du graphique
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
    
    # Titre
    bee_info = df[df['id'] == bee_id].iloc[0]
    plt.title(f'Arbre Généalogique - Abeille {bee_id}\n'
              f'Distance: {bee_info["distance"]:.2f} • '
              f'Génération: {bee_info["generation"]}', 
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
    
    # Information en bas
    ax.text(0.5, -0.15, f'{len(ancestors)} abeilles • {len(generations)} générations', 
            transform=ax.transAxes, ha='center', va='center',
            fontsize=10, color='#7F8C8D', style='italic',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

# Utilisation
if __name__ == "__main__":
    df = load_bee_data()
    plot_genealogy_tree(df, 500)