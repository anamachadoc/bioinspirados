from Ant import Ant
from typing import Any, Dict
import random
import matplotlib.pyplot as plt
import copy
from statistics import mean, median, stdev
import numpy as np
import os

class AntColony():
    def __init__(self, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.ant_config = kwargs
        self.ants = self._init_ants()
        self.pheromone_matrix = self._init_pheromone()
        os.makedirs(self.output_path, exist_ok=True)
    
    def _init_ants(self):
        return [Ant(i, **self.ant_config) for i in range(self.n_cities)]
        
    def _init_pheromone(self):
        return {
            i: {
                j: self.initial_pheromone if i != j else 0.0
                for j in range(self.n_cities)
            }
            for i in range(self.n_cities)}
    
    def get_ants(self):
        return self.ants
    
    def get_pheromone_matrix(self):
        return self.pheromone_matrix
            