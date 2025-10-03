import pandas as pd


class GenealogyTree:
    """Classe pour gérer l'arbre généalogique des abeilles (logique uniquement)"""
    
    def __init__(self, csv_filepath='bees_log.csv'):
        """
        Initialise l'arbre généalogique à partir d'un fichier CSV
        
        Args:
            csv_filepath (str): Chemin vers le fichier CSV des abeilles
        """
        self.df = pd.read_csv(csv_filepath)
        # Créer un dictionnaire pour un accès O(1) au lieu de O(n)
        self.df_dict = {row['id']: row for _, row in self.df.iterrows()}
    
    def get_bee_info(self, bee_id):
        """
        Récupère les informations d'une abeille
        
        Args:
            bee_id (int): ID de l'abeille
            
        Returns:
            dict: Informations de l'abeille ou None si non trouvée
        """
        if bee_id not in self.df_dict:
            return None
        return dict(self.df_dict[bee_id])
    
    def get_ancestors(self, bee_id):
        """
        Récupère tous les ancêtres d'une abeille donnée (VERSION ITERATIVE - sans récursion)
        
        Args:
            bee_id (int): ID de l'abeille à analyser
            
        Returns:
            dict: Dictionnaire des ancêtres avec leur génération et parents
        """
        if bee_id not in self.df_dict:
            return {}
        
        ancestors = {}
        # File d'attente : (bee_id, generation)
        to_process = [(bee_id, 0)]
        processed = set()
        
        while to_process:
            current_id, generation = to_process.pop(0)
            
            # Éviter les doublons
            if current_id in processed:
                continue
            processed.add(current_id)
            
            # Vérifier que l'abeille existe
            if current_id not in self.df_dict:
                continue
            
            bee = self.df_dict[current_id]
            ancestors[current_id] = {
                'generation': generation,
                'parent_1': bee['parent_1'],
                'parent_2': bee['parent_2']
            }
            
            # Ajouter les parents à traiter
            if pd.notna(bee['parent_1']):
                parent_1_id = int(bee['parent_1'])
                if parent_1_id not in processed:
                    to_process.append((parent_1_id, generation + 1))
            
            if pd.notna(bee['parent_2']):
                parent_2_id = int(bee['parent_2'])
                if parent_2_id not in processed:
                    to_process.append((parent_2_id, generation + 1))
        
        return ancestors
    
    def organize_by_generation(self, ancestors):
        """
        Organise les ancêtres par génération
        
        Args:
            ancestors (dict): Dictionnaire des ancêtres
            
        Returns:
            dict: Dictionnaire {génération: [liste d'IDs]}
        """
        generations = {}
        for bee_id_key, info in ancestors.items():
            gen = info['generation']
            if gen not in generations:
                generations[gen] = []
            generations[gen].append(bee_id_key)
        return generations
    
    def calculate_positions(self, generations):
        """
        Calcule les positions (x, y) de chaque abeille dans l'arbre
        
        Args:
            generations (dict): Dictionnaire organisé par génération
            
        Returns:
            dict: {bee_id: (x, y)}
        """
        positions = {}
        for gen in sorted(generations.keys()):
            bees = generations[gen]
            y = gen * 2.0
            total_width = (len(bees) - 1) * 2.5
            start_x = -total_width / 2
            
            for i, bee_id_key in enumerate(bees):
                x = start_x + i * 2.5
                positions[bee_id_key] = (x, y)
        
        return positions
