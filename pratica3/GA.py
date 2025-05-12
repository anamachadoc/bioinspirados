from Knapsack import Knapsack
import numpy as np
import os
import random
from statistics import mean, median, stdev
import copy
import matplotlib.pyplot as plt

class GeneticAlgorithm():
  def __init__(self, save_path, **kwargs):
    for key, value in kwargs.items():
        setattr(self, key, value)
    self.parents = None
    self.best_fitness_per_generation = []
    self.population = [Individual(individual, **self.config_individual) 
        for individual in [
            np.random.uniform(low=self.config_individual['x_min'], high=self.config_individual['x_max'], size=(self.config_individual['n_parameters'])) 
            for _ in range(self.n_pop)]
    ]
    self.population_aux = []
    self.best_solutions = self.get_best_solutions()[:2]
    self.n_pop = self.n_pop if self.n_pop % 2 == 0 else self.n_pop - 1
    self.save_data = save_path
    os.makedirs(self.save_data) if not os.path.exists(self.save_data) else None
    print(self.save_data)
    
  def get_best_solutions(self):
    sorted_population = sorted(self.population, key=lambda x: x.get_fitness())
    return sorted_population

  def get_pop(self, pop, file):
    for p in pop:
      a = p.get_chromosome()
      b = p.get_fitness()
      file.write(f'{a}, {b}\n')

  def get_fitness_population(self):
    return [x.get_fitness() for x in self.population]
  
  def roulette(self):
    parents = []
    sum_fitness = sum([p.get_inverted_fitness() for p in self.population])
    roulette_values = [p.get_inverted_fitness()/sum_fitness for p in self.population]
    i = 0
    while( i < self.n_pop):
      random_value = random.random()
      accumulated_sum = 0
      for j, prob in enumerate(roulette_values):  
          accumulated_sum += prob
          if accumulated_sum >= random_value:
              parents.append(self.population[j])
              i = i + 1
              break  
    return parents

  def get_crossing_alpha_beta(self):
    new_generation = []
    for i in range(0, len(self.parents), 2):
        p1, p2 = self.parents[i], self.parents[i + 1]
        X, Y = (p1, p2) if p1.get_fitness() > p2.get_fitness() else (p2, p1)
        X_chrom = X.get_chromosome()
        Y_chrom = Y.get_chromosome()
        child1_genes = []
        child2_genes = []
        for x_gene, y_gene in zip(X_chrom, Y_chrom):
            d = x_gene - y_gene
            min_val = y_gene - self.beta * d
            max_val = x_gene + self.alpha * d
            child1_genes.append(random.uniform(min_val, max_val))
            child2_genes.append(random.uniform(min_val, max_val))
        child1 = Individual(child1_genes, **self.config_individual)
        child2 = Individual(child2_genes, **self.config_individual)
        new_generation.extend([child1, child2])
    return new_generation

  def get_mutation(self):
    for i in range(self.n_pop):
        chromosome = self.population_aux[i].get_chromosome()
        mutated = False
        mutated_genes = []
        for gene in chromosome:
            new_gene = np.random.uniform(low=self.config_individual['x_min'], high=self.config_individual['x_max']) if random.random() <= self.prob_mutation else gene
            if new_gene != gene:
                mutated = True
                mutated_genes.append(new_gene)
        if mutated:
            self.population_aux[i] = copy.deepcopy(Individual(mutated_genes, **self.config_individual))
            
  def get_elitism(self):
    best_individuals = self.best_solutions
    position = random.sample(range(self.n_pop), k=len(best_individuals))
    for i, elite in enumerate(best_individuals):
        self.population_aux[position[i]] = copy.deepcopy(elite)
    return self.population_aux

  def run(self):
    generation = 0
    while (generation < self.n_gen):
        self.best_fitness_per_generation.append(self.best_solutions[0].get_fitness())
        self.save_data_generation(generation)
        self.parents = self.roulette()
        self.population_aux = copy.deepcopy(self.get_crossing_alpha_beta())
        self.get_mutation()
        if self.elitism:
          self.population = self.get_elitism()
        else:
          self.population = self.population_aux
        self.best_solutions = self.get_best_solutions()[:self.n_elite]
        generation += 1
        
    self.plot_fitness()
    self.save_fitness()

  # used to observe the evolution of fitness in the best set of parameters
  def save_data_generation(self, generation): 
    with open(f'{self.save_data}/data_generation.txt', 'a') as file:
        sorted_solutions = self.get_best_solutions()
        best_fitness = sorted_solutions[0].get_fitness()
        worst_fitness = sorted_solutions[self.n_pop-1].get_fitness()
        mean_fitness = mean(self.get_fitness_population())
        median_fitness = median(self.get_fitness_population())
        file.write(f'{generation} {best_fitness} {worst_fitness} {mean_fitness} {median_fitness}\n')

  def plot_fitness(self):
        plt.plot(self.best_fitness_per_generation)
        plt.title('Best Fitness Across Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.grid(True)
        plt.savefig(f'{self.save_data}/best_fitness.png')
        #plt.show()
        
  def save_fitness(self):
    best_fitness = self.best_solutions[0].get_fitness()
    mean_fitness = mean(self.get_fitness_population())
    stdev_fitness = stdev(self.get_fitness_population())
    with open(f'{self.save_data}/data_fitness.txt', 'w') as file:
      file.write(f'{best_fitness} {mean_fitness} {stdev_fitness}')