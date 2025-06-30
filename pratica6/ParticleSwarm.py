from Particle import Particle 
from typing import Any, Dict
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from statistics import mean, median, stdev

class ParticleSwarm():
    def __init__(self, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        os.makedirs(self.output_path, exist_ok=True)
        self.particles = [Particle(np.random.uniform(low=self.x_limits[0], high=self.x_limits[1], size=self.num_dimensions), **kwargs)
        for p in range(self.num_pop)]
        self.best_fitness_per_generation = []
        self.positions_through_generation = []
        self._define_neighborhood()
        self._att_pbest()
        self._att_gbest()
        self.best_fitness = None
        self.stagnation_counter = 0
        self.stopping_iteration = self.max_iteration 
        
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

    def get_best_solutions(self):
        sorted_particles = sorted(self.particles, key=lambda particle: particle.get_fitness())
        return sorted_particles   
      
    def plot_fitness(self):
        plt.plot(self.best_fitness_per_generation)
        plt.title('Best Fitness Across Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.grid(True)
        plt.savefig(f'{self.output_path}/best_fitness.png')
        
    def save_fitness(self):
        best_fitness = self.get_best_solutions()[0].get_fitness()
        mean_fitness = mean(self.get_fitness_particles())
        stdev_fitness = stdev(self.get_fitness_particles())
        with open(f'{self.output_path}/data_fitness.txt', 'w') as file:
            file.write(f'{best_fitness} {mean_fitness} {stdev_fitness}')
       
    def get_fitness_particles(self):
        return [x.get_fitness() for x in self.particles]
 
    def save_data_generation(self, generation): 
        with open(f'{self.output_path}/data_generation.txt', 'a') as file:
            sorted_solutions = self.get_best_solutions()
            best_fitness = sorted_solutions[0].get_fitness()
            worst_fitness = sorted_solutions[self.num_pop-1].get_fitness()
            mean_fitness = mean(self.get_fitness_particles())
            median_fitness = median(self.get_fitness_particles())
            file.write(f'{generation} {best_fitness} {worst_fitness} {mean_fitness} {median_fitness}\n')

    def att_positions(self):
        self.positions_through_generation.append(np.array([p.get_position() for p in self.particles]))


    def animate_particles(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scat = ax.scatter([], [], [], s=50)
        def init():
            ax.set_xlim(self.x_limits[0], self.x_limits[1])
            ax.set_ylim(self.x_limits[0], self.x_limits[1])
            ax.set_zlim(self.x_limits[0], self.x_limits[1])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Convergência das Partículas')
            return scat,
        def update(frame):
            data = self.positions_through_generation[frame]
            scat._offsets3d = (data[:, 0], data[:, 1], data[:, 2])
            ax.set_title(f'Geração {frame}')
            return scat,
        anim = FuncAnimation(
        fig, update, frames=len(self.positions_through_generation),
        init_func=init, blit=False, interval=200
        )

        output_file = os.path.join(self.output_path, '3d_animate.mp4')
        anim.save(output_file.replace(".mp4", ".gif"), writer='pillow', fps=5)

    def save_stopping_iteration(self):
        with open(f'{self.output_path}/stopping_iteration.txt', "w") as f:
            f.write(f"{self.stopping_iteration}\n")
            
    def run(self):
        iteration = 0 
        while iteration < self.max_iteration:
            for p in self.particles:
                p.att_particle()
            self._att_pbest()
            self._att_gbest()
            self._define_neighborhood()
            
            self.save_data_generation(iteration)
            current_best_fitness = self.get_best_solutions()[0].get_fitness()
            self.best_fitness_per_generation.append(current_best_fitness)

            if self.best_fitness is not None and np.isclose(current_best_fitness, self.best_fitness, rtol=1e-8):
                stagnation_counter += 1
            else:
                stagnation_counter = 0
                self.best_fitness = current_best_fitness

            if stagnation_counter >= 50:
                print(f"Stopping due to stagnation at iteration {iteration}")
                self.stopping_iteration = iteration
                break
            
            self.att_positions()
            iteration += 1

        self.plot_fitness()
        self.save_fitness()
        self.animate_particles()
        self.save_stopping_iteration()


