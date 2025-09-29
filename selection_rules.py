import random

def create_child(parent_1, parent_2, all_nodes, hive):
    child = [hive]
    visited = set(child)

    # arêtes des parents
    edges_1 = [(parent_1[i], parent_1[i+1]) for i in range(len(parent_1)-1)]
    edges_2 = [(parent_2[i], parent_2[i+1]) for i in range(len(parent_2)-1)]

    # version non-orientée pour comparaison
    set_edges_1 = {frozenset((a, b)) for a, b in edges_1}
    set_edges_2 = {frozenset((a, b)) for a, b in edges_2}

    # arêtes communes (sans orientation)
    common_edges = set_edges_1 & set_edges_2

    # construction enfant avec orientation aléatoire
    for edge_set in common_edges:
        # récupérer les orientations possibles (dans chaque parent)
        orientations = []
        for (a, b) in edges_1 + edges_2:
            if frozenset((a, b)) == edge_set:
                orientations.append((a, b))

        if orientations:
            a, b = random.choice(orientations)  # tirage au sort de l'orientation

            if a not in visited:
                child.append(a)
                visited.add(a)
            if b not in visited:
                child.append(b)
                visited.add(b)

    # compléter avec les autres noeuds aléatoirement
    remaining = [n for n in all_nodes if n not in visited]
    while remaining:
        next_node = random.choice(remaining)
        child.append(next_node)
        visited.add(next_node)
        remaining.remove(next_node)

    child.append(hive)
    return child

def create_child_order_crossover(parent_1, parent_2, all_nodes, hive):
    # Algorithme Order Crossover (OX)
    
    # Supprimer la ruche du début et fin pour le croisement
    genes_1 = parent_1[1:-1]  # sans la ruche
    genes_2 = parent_2[1:-1]  # sans la ruche
    
    size = len(genes_1)
    
    # Choisir deux points de coupure aléatoires
    start, end = sorted(random.sample(range(size), 2))
    
    # Initialiser l'enfant avec des None
    child = [None] * size
    
    # Copier le segment entre start et end du parent 1 vers l'enfant
    child[start:end] = genes_1[start:end]
    
    # Remplir le reste avec les gènes du parent 2 dans l'ordre
    current_pos = end
    parent_pos = end
    
    # Parcourir le parent 2 à partir de end pour remplir les cases vides
    for i in range(size):
        if current_pos >= size:
            current_pos = 0
        if parent_pos >= size:
            parent_pos = 0
            
        gene = genes_2[parent_pos]
        if gene not in child:  # Si le gène n'est pas déjà dans l'enfant
            child[current_pos] = gene
            current_pos += 1
        
        parent_pos += 1
        
        # Si l'enfant est complet, sortir
        if None not in child:
            break
    
    # Réajouter la ruche au début et à la fin
    child_with_hive = [hive] + child + [hive]
    
    return child_with_hive
