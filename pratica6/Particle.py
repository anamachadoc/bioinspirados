from typing import Any, Dict
import os
import random
import numpy as np

class Particle():
    def __init__(self, position: np.ndarray, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.position = position
        self.speed = 0

    def get_position(self):
        return self.position
    
    def get_speed(self):
        return self.speed
    
    def new_speed(self):
        r1, r2 = random.random(), random.random()
