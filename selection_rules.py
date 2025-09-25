import random

def create_child(parent_1, parent_2, all_nodes, hive):
 # all_nodes = > tous les noeuds du graph (y compris la ruche)
 # hive => ruche (départ et arrivée , incompressible)

    child = [hive] # initialistion de la liste enfant avec le départ
    vistited = set(child) # Garantie:1 noeud = 1 visite set() évite les doublons

 # modèle de construction des listes, pour chaque parents, des arrêtes
    edges_1 = [(parent_2[i], parent_2[i+1] for i in range(len(parent_2)-1))]
    edges_2 = [(parent_2[i], parent_2[i+1] for i in range(len(parent_2)-1))]

# selection des arêtes communes aux deux parents pour transmission
    set_edges_1 = set(tuple(sorted((a,b))) for a,b in edges_1)
    # sorted((a, b)) => trie les paires par odre croissant. Ex: (3,0) => (0,3)
    # tuple(...) => créé un objet immuable & comparable
    # set() créé un ensemble d'éléments uniques => doublons prohibés
    set_edges_2 = set(tuple(sorted((a,b))) for a,b in edges_2)

    # & => opérateur d'insertion dans set() python, garde uniquement les éléments communs aux deux ensembles
    common_edges =set_edges_1 & set_edges_2 
    
