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
