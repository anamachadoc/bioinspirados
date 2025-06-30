from typing import Any, Dict
import os
import random
import numpy as np
import math

class Particle():
    def __init__(self, position: np.ndarray, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.position = position
        self.pbest = position
        self.gbest = None
        self.speed = np.zeros(self.num_dimensions)
        self.fitness = self.function_fitness(self.position)
        self.neighbors = []

    def get_position(self):
        return self.position
    
    def get_speed(self):
        return self.speed

    def get_fitness(self):
        return self.fitness
    
    def get_neighbors(self):
        return self.neighbors
    
    def get_gbest(self):
        return self.gbest
    
    def get_pbest(self):
        return self.pbest
    
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
    
    def set_pbest(self):
        if self.function_fitness(self.position) < self.function_fitness(self.pbest):
            self.pbest = self.position
        
    def set_gbest(self):
        best_neighbor = min(self.neighbors, key=lambda p: p.get_fitness())
        if self.gbest is None or best_neighbor.get_fitness() < self.function_fitness(self.gbest):
            self.gbest = best_neighbor.get_position()
    
    def _new_speed(self):
        if self.gbest is None:
            return
        r1, r2 = random.random(), random.random()
        diversity = self.w * self.speed
        individual_intensification = self.c1 * r1 * (self.pbest - self.position)
        social_intensification = self.c2 * r2 * (self.gbest - self.position)
        self.speed = diversity + individual_intensification + social_intensification
    
    def _new_position(self):
        self.position = self.position + self.speed
    
    def function_fitness(self, position):
        return -20 * pow(math.e, (-0.2 * math.sqrt(1/self.num_dimensions * sum(x**2 for x in position)))) - pow(math.e, 1/self.num_dimensions * sum(math.cos(2 * math.pi * x) for x in position)) + 20 + math.e
    
    def att_particle(self):
        self._new_speed()
        self._new_position()
        self.fitness = self.function_fitness(self.position)