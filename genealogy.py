import pandas as pd


class GenealogyTree:
    """Gère l'arbre généalogique des abeilles"""
    
    def __init__(self, csv_filepath='bees_log.csv'):
        """Charge les données des abeilles depuis le CSV"""
        self.df = pd.read_csv(csv_filepath)
        # Index rapide : {id_abeille: données_abeille}
        self.abeilles = {row['id']: row for _, row in self.df.iterrows()}
    
    def get_bee_info(self, bee_id):
        """Retourne les infos d'une abeille ou None si inexistante"""
        return dict(self.abeilles[bee_id]) if bee_id in self.abeilles else None
    
    def get_ancestors(self, bee_id):
        """
        Trouve tous les ancêtres d'une abeille (algorithme itératif)
        Retourne: {id_abeille: {'generation': niveau, 'parent_1': id, 'parent_2': id}}
        """
        if bee_id not in self.abeilles:
            return {}
        
        ancestors = {}
        a_traiter = [(bee_id, 0)]  # (id_abeille, niveau_dans_arbre)
        deja_traites = set()
        
        while a_traiter:
            current_id, niveau = a_traiter.pop(0)
            
            if current_id in deja_traites or current_id not in self.abeilles:
                continue
            
            deja_traites.add(current_id)
            bee = self.abeilles[current_id]
            
            # Enregistrer cette abeille
            ancestors[current_id] = {
                'generation': niveau,
                'parent_1': bee['parent_1'],
                'parent_2': bee['parent_2']
            }
            
            # Ajouter les parents à traiter
            for parent_col in ['parent_1', 'parent_2']:
                if pd.notna(bee[parent_col]):
                    parent_id = int(bee[parent_col])
                    if parent_id not in deja_traites:
                        a_traiter.append((parent_id, niveau + 1))
        
        return ancestors
    
    def organize_by_level(self, ancestors):
        """Groupe les abeilles par niveau généalogique"""
        niveaux = {}
        for bee_id, info in ancestors.items():
            niveau = info['generation']
            if niveau not in niveaux:
                niveaux[niveau] = []
            niveaux[niveau].append(bee_id)
        return niveaux
    
    def calculate_positions(self, niveaux):
        """Calcule la position (x, y) de chaque abeille pour l'affichage"""
        positions = {}
        
        for niveau, abeilles in sorted(niveaux.items()):
            y = niveau * 2.0  # Niveau 0 en bas, ancêtres en haut 
            
            # Répartir horizontalement
            nb_abeilles = len(abeilles)
            largeur_totale = (nb_abeilles - 1) * 2.5
            x_debut = -largeur_totale / 2
            
            for i, bee_id in enumerate(abeilles):
                x = x_debut + i * 2.5
                positions[bee_id] = (x, y)
        
        return positions