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
        self.speed = np.zeros(self.num_dimensions)
        self.fitness = self.function_fitness()

    def get_position(self):
        return self.position
    
    def get_speed(self):
        return self.speed

    def get_fitness(self):
        return self.fitness
    
    def _new_speed(self, gbest):
        r1, r2 = random.random(), random.random()
        diversity = self.w * self.speed
        individual_intensification = self.c1 * r1 * (self.pbest - self.position)
        social_intensification = self.c2 * r2 * (gbest - self.position)
        return diversity + individual_intensification + social_intensification
    
    def _new_position(self):
        return self.position + self.speed
    
    def function_fitness(self):
        return -20 * pow(math.e, (-0.2 * math.sqrt(1/self.num_dimensions * sum(x**2 for x in self.position)))) - pow(math.e, 1/self.num_dimensions * sum(math.cos(2 * math.pi * x) for x in self.position)) + 20 + math.e
    
    def att_particle(self):
        self._new_speed()
        self._new_position()