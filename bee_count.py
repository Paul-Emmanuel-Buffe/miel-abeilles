import pandas as pd
from datetime import datetime

class MrBee:
    def __init__(self):
        # DataFrame vide pour stocker toutes les abeilles
        self.bees_df = pd.DataFrame(columns=[
            "id", "simulation_id", "generation", "distance",
            "parent_1", "parent_2", "chemin", "timestamp"
        ])
        self.next_id = 1  # compteur automatique d'ID

    def add_bee(self, simulation_id, generation, distance, parent_1, parent_2, chemin):
        """
        Enregistre une abeille et renvoie son ID.
        """
        bee_id = self.next_id
        self.next_id += 1

        self.bees_df.loc[len(self.bees_df)] = {
            "id": bee_id,
            "simulation_id": simulation_id,
            "generation": generation,
            "distance": distance,
            "parent_1": parent_1,
            "parent_2": parent_2,
            "chemin": chemin,
            "timestamp": datetime.now()
        }
        return bee_id

    def save_csv(self, filename):
        """
        Sauvegarde le DataFrame actuel dans un fichier CSV.
        """
        self.bees_df.to_csv(filename, index=False)
