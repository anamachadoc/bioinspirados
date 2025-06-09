from Ant import Ant
from typing import Any, Dict
import random
import matplotlib.pyplot as plt
import os
from statistics import mean, median, stdev
import random

class AntColony():
    def __init__(self, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.ant_config = kwargs
        self.ants = self._init_ants()
        self.pheromone_matrix = self._init_pheromone()
        self.best_ant_global = None
        self.best_fitness_per_generation = []
        self.fitness_ant_0 = []
        os.makedirs(self.output_path, exist_ok=True)
    
    def _init_ants(self):
        return [Ant(i, **self.ant_config) for i in range(1, self.n_cities + 1)]
        
    def _init_pheromone(self):
        return {
            i: {
                j: self.initial_pheromone if i != j else 0.0
                for j in range(1, self.n_cities + 1)
            }
            for i in range(1, self.n_cities + 1)
        }
    
    def get_ants(self):
        return self.ants
    
    def get_pheromone_matrix(self):
        return self.pheromone_matrix
       
    def get_best_solutions(self):
        sorted_ants = sorted(self.ants, key=lambda ant: ant.get_fitness())
        return sorted_ants
     
    def run(self):
        cont = 0
        while cont < self.max_iteration:
            order_ants = random.sample(range(0, self.n_cities), self.n_cities)
            for i in order_ants: 
                self.ants[i].new_path(self.pheromone_matrix)
            best_ant_iter = self.get_best_solutions()[0]
            best_ant_iter.best_ant_pheromone(self.pheromone_matrix)
            cont += 1 
            self.best_fitness_per_generation.append(best_ant_iter.get_fitness())
            self.save_data_generation(cont)  
            self.fitness_ant_0.append(self.ants[0].get_fitness())
        self.plot_fitness()
        self.save_fitness()
        self.plot_ant_0_fitness()
      
    def plot_fitness(self):
        plt.plot(self.best_fitness_per_generation)
        plt.title('Best Fitness Across Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.grid(True)
        plt.savefig(f'{self.output_path}/best_fitness.png')
        
    def save_fitness(self):
        best_fitness = self.get_best_solutions()[0].get_fitness()
        mean_fitness = mean(self.get_fitness_paths())
        stdev_fitness = stdev(self.get_fitness_paths())
        with open(f'{self.output_path}/data_fitness.txt', 'w') as file:
            file.write(f'{best_fitness} {mean_fitness} {stdev_fitness}')
       
    def get_fitness_paths(self):
        return [x.get_fitness() for x in self.ants]
 
    def save_data_generation(self, generation): 
        with open(f'{self.output_path}/data_generation.txt', 'a') as file:
            sorted_solutions = self.get_best_solutions()
            best_fitness = sorted_solutions[0].get_fitness()
            worst_fitness = sorted_solutions[self.n_cities-1].get_fitness()
            mean_fitness = mean(self.get_fitness_paths())
            median_fitness = median(self.get_fitness_paths())
            file.write(f'{generation} {best_fitness} {worst_fitness} {mean_fitness} {median_fitness}\n')
            
    def plot_ant_0_fitness(self):
        plt.figure()
        plt.plot(self.fitness_ant_0, label='Fitness da Formiga 0', color='orange')
        plt.title('Fitness da Formiga 0 por Geração')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.legend()
        plt.savefig(f'{self.output_path}/fitness_ant_0.png')

    