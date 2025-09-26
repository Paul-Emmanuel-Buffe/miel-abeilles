import random

def create_child(parent_1, parent_2, all_nodes, hive):
    # all_nodes = > tous les noeuds du graph (y compris la ruche)
    # hive => ruche (départ et arrivée , incompressible)

    child = [hive] # initialistion de la liste enfant avec le départ
    visited = set(child) # Garantie:1 noeud = 1 visite set() évite les doublons

 
    # modèle de construction des listes, pour chaque parents, des arrêtes
    edges_1 = [(parent_1[i], parent_1[i+1]) for i in range(len(parent_1)-1)]
    edges_2 = [(parent_2[i], parent_2[i+1]) for i in range(len(parent_2)-1)]


    # selection des arêtes communes aux deux parents pour transmission
    set_edges_1 = set(tuple(sorted((a,b))) for a,b in edges_1)
    # sorted((a, b)) => trie les paires par odre croissant. Ex: (3,0) => (0,3)
    # tuple(...) => créé un objet immuable & comparable
    # set() créé un ensemble d'éléments uniques => doublons prohibés
    set_edges_2 = set(tuple(sorted((a,b))) for a,b in edges_2)

    # & => opérateur d'insertion dans set() python, garde uniquement les éléments communs aux deux ensembles
    common_edges =set_edges_1 & set_edges_2 


    # construction du chemin enfant:
    # 1 seul parent considérer car on à déjà filtré les arêtes communes avec common_edges
    # Si un pattern d'association d'arêtes est observé chez les deux parents il est conservé
    for i in range(len(parent_1)-1):
        
        a, b = parent_1[i], parent_1[i+1] # création des arêtes(tuple)
        edge = tuple(sorted((a,b)))

        if edge in common_edges: # condition pour garder les arêtes commune des deux parents

            if a not in visited: # condition pour éviter de visiter des noeud déjà vistés
                child.append(a)
                visited.add(a)

            if b not in visited: # idem
                child.append(b)
                visited.add(b)   


    # complète les autres noeuds aléatoirement
    remaining = [n for n in all_nodes if n not in visited ] 

    while remaining:
        next_node = random.choice(remaining)
        child.append(next_node)
        visited.add(next_node)
        remaining.remove(next_node)

    child.append(hive)

    return child
