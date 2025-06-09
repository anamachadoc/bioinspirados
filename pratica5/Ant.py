from Path import Path 
from typing import Any, Dict
import os

class Ant():
    def __init__(self, starting_city, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.starting_city = starting_city
        self.path_aux = []
        self.path = None
        os.makedirs(self.output_path, exist_ok=True)
    
    def _define_path(self, pheromone_matrix):
        self.path_aux = [self.starting_city]
        while len(self.path_aux) < self.n_cities:
            probabilities = self._get_probability_cities(pheromone_matrix, self.path_aux[-1])
            if not probabilities:
                break
            next_city = max(probabilities, key=probabilities.get)
            self.local_pheromone(pheromone_matrix, self.path_aux[-1], next_city)
            self.path_aux.append(next_city)
        self.path_aux.append(self.starting_city)
        return self.path_aux
        
    def _get_probability_cities(self, pheromone_matrix, i_city):
        attractiveness = {
            j: pow(pheromone_matrix[i_city][j], self.alpha) *
               pow(1.0 / self.distance_cities[i_city][j], self.beta)
            for j in self.possible_cities
            if j not in self.path_aux
        }
        total_attractiveness = sum(attractiveness.values())
        if total_attractiveness == 0:
            return {}
        probabilities = {
            j: a_j / total_attractiveness
            for j, a_j in attractiveness.items()
        }
        return probabilities

    def get_path(self):
        return self.path
     
    def get_fitness(self): 
        if self.path is None:
            raise ValueError("Path ainda não definido. Chame new_path() antes.")
        return self.path.get_distance()
       
    def local_pheromone(self, pheromone_matrix, i_city, j_city):
        pheromone_matrix[i_city][j_city] = (
            (1 - self.refresh_rate) * pheromone_matrix[i_city][j_city]
            + self.refresh_rate * self.initial_pheromone
        )
        
    def best_ant_pheromone(self, pheromone_matrix):
        path_distance = self.path.get_distance()
        deposit_amount = self.Q / path_distance
        for i in range(self.path.get_num_cities()):
            current_city = self.path.get_ordered_cities()[i]
            next_city = self.path.get_ordered_cities()[(i + 1) % self.path.get_num_cities()] 
            pheromone_matrix[current_city][next_city] = (
                (1 - self.evaporation_rate) * pheromone_matrix[current_city][next_city]
                + self.evaporation_rate * deposit_amount
            )

    def new_path(self, pheromone_matrix):
        self.path = Path(self._define_path(pheromone_matrix), self.distance_cities, self.coordenates_cities)
