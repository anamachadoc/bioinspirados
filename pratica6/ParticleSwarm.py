from Particle import Particle 
from typing import Any, Dict
import os
import numpy as np

class ParticleSwarm():
    def __init__(self, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        os.makedirs(self.output_path, exist_ok=True)
        self.particles = [Particle(np.random.uniform(low=self.x_limits[0], high=self.x_limits[1], size=self.num_dimensions), **kwargs)
        for p in range(self.num_pop)]
        
    def get_population(self):
        return self.particles
    
    def get_gbest(self):
        