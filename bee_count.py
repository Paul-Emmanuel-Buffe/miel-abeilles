import pandas as pd
from datetime import datetime


import pandas as pd
from datetime import datetime


#  Infos de toutes les abeilles générées
class MrBee:          

# id             : id abeille
# simulation_id  : id de la simulation (main => 'simulation_id = 1' )
# generation     : génération de l'abeille 
# distance       : distance parcourue par l'abeille
# parent_1       : id parent 1
# parent_2       : id parent 2
# chemin         : parcours sous forme de liste
# n_generations  : nombre total de générations de la simulation
# mutation_rate  : taux de mutation utilisé
# elitisme_rate  : taux d'élitisme de cette génération
# timestamp      : Date & heure de l'enregistrement
    
    def __init__(self):
        # DataFrame vide pour stocker toutes les abeilles
        self.bees_df = pd.DataFrame(columns=[
            "id", "simulation_id", "generation", "distance",
            "parent_1", "parent_2", "chemin", "n_generations",
            "mutation_rate", "elitisme_rate", "timestamp"
        ])
        self.next_id = 1  # compteur automatique d'ID

    def add_bee(self, simulation_id, generation, distance, parent_1, parent_2, chemin, 
                n_generations, mutation_rate, elitisme_rate):
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
            "n_generations": n_generations,
            "mutation_rate": mutation_rate,
            "elitisme_rate": elitisme_rate,
            "timestamp": datetime.now()
        }
        return bee_id

    def save_csv(self, filename):
        """
        Sauvegarde le DataFrame actuel dans un fichier CSV.
        """
        self.bees_df.to_csv(filename, index=False)