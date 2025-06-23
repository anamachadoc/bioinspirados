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
        self._define_neighborhood()
        self._att_pbest()
        self._att_gbest()
        
    def _define_neighborhood(self):
        if self.topology == 'global':
            self._set_global_topology()
        elif self.topology == 'ring':
            self._set_ring_topology()
        elif self.topology == 'focal':
            self._set_focal_topology()
        else:
            raise ValueError(f"invalid topology: {self.topology}")

    def _set_global_topology(self):
        for particle in self.particles:
            particle.set_neighbors(self.particles)

    def _set_ring_topology(self):
        for i, particle in enumerate(self.particles):
            neighborhood = [
                self.particles[(i - 1) % self.num_pop],
                self.particles[(i + 1) % self.num_pop],
                particle
            ]
            particle.set_neighbors(neighborhood)

    def _set_focal_topology(self):
        focal = min(self.particles, key=lambda p: p.get_fitness())
        for particle in self.particles:
            if particle is focal:
                neighborhood = self.particles
            else:
                neighborhood = [focal]
            particle.set_neighbors(neighborhood)

    def _att_pbest(self):
        for p in self.particles:
            p.set_pbest()
          
    def _att_gbest(self):
        for p in self.particles:
            p.set_gbest()
                
    def get_population(self):
        return self.particles   
    
    def get_gbest(self, particle):
        return min(particle.get_neighbors(), key=lambda p: p.get_fitness())
    
    def get_best_solution(self):
        p = min(self.particles, key=lambda p: p.function_fitness(p.get_gbest()))
        return p.get_gbest(), p.function_fitness(p.get_gbest())
        
    def run(self):
        iteration = 0
        while iteration < self.max_iteration:
            for p in self.particles:
                p.att_particle()
            self._att_pbest()
            self._att_gbest()
            print(f'iteracao {iteration} - {self.get_best_solution()}')
            self._define_neighborhood()
            iteration += 1
