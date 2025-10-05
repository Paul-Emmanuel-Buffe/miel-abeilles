import pandas as pd

class GenealogyTree:
    # gère l'arbre généalogique des abeilles

    def __init__(self, csv_filepath='bees_log.csv'):
        # charge les données depuis le csv
        self.df = pd.read_csv(csv_filepath)
        # crée un index rapide pour accéder aux abeilles par id
        self.abeilles = {row['id']: row for _, row in self.df.iterrows()}

    def get_bee_info(self, bee_id):
        # retourne les informations d'une abeille ou none si elle n'existe pas
        return dict(self.abeilles[bee_id]) if bee_id in self.abeilles else None

    def get_ancestors(self, bee_id):
        # retourne tous les ancêtres d'une abeille
        # format: {id_abeille: {'generation': niveau, 'parent_1': id, 'parent_2': id}}
        
        # si l'abeille n'existe pas, retourner dictionnaire vide
        if bee_id not in self.abeilles:
            return {}

        ancestors = {}  # dictionnaire pour stocker les ancêtres
        a_traiter = [(bee_id, 0)]  # file d'attente avec tuples (id_abeille, niveau)
        deja_traites = set()       # ensemble pour éviter de traiter plusieurs fois la même abeille

        # parcours itératif pour récupérer tous les ancêtres
        while a_traiter:
            current_id, niveau = a_traiter.pop(0)  # récupérer l'abeille et son niveau
            # ignorer si déjà traité ou inexistant
            if current_id in deja_traites or current_id not in self.abeilles:
                continue

            deja_traites.add(current_id)  # marquer comme traité
            bee = self.abeilles[current_id]  # récupérer les infos de l'abeille

            # enregistrer l'abeille et ses parents
            ancestors[current_id] = {
                'generation': niveau,
                'parent_1': bee['parent_1'],
                'parent_2': bee['parent_2']
            }

            # ajouter les parents à la file d'attente avec niveau +1
            for parent_col in ['parent_1', 'parent_2']:
                if pd.notna(bee[parent_col]):  # vérifier que le parent existe
                    parent_id = int(bee[parent_col])
                    if parent_id not in deja_traites:
                        a_traiter.append((parent_id, niveau + 1))

        return ancestors
