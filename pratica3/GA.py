from Knapsack import Knapsack
from Item import Item
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
    self.kwargs = kwargs
    self.num_items = 0
    self.items = self.get_items()
    self.parents = None
    self.best_fitness_per_generation = []
    self.population = [Knapsack(self.items, [random.randint(0, 1) for _ in range(self.num_items)], **kwargs) 
          for _ in range(self.n_pop)]
    self.population_aux = []
    self.best_solutions = self.get_best_solutions()[:2]
    self.n_pop = self.n_pop if self.n_pop % 2 == 0 else self.n_pop - 1
    self.save_data = save_path
    os.makedirs(self.save_data) if not os.path.exists(self.save_data) else None
  
  def get_items(self):
    with open(self.path_p, 'r') as f_p, open(self.path_w, 'r') as f_w:
        utilities = list(map(int, map(str.strip, f_p)))
        weights = list(map(int, map(str.strip, f_w)))
    
    self.num_items = len(utilities)
    return [Item(i, w, u) for i, (w, u) in enumerate(zip(weights, utilities))]
  
  def get_best_solutions(self):
    sorted_population = sorted(self.population, key=lambda x: x.get_fitness(), reverse=True)
    return sorted_population

  def get_pop(self, pop, file):
    for p in pop:
      a = p.get_set_items()
      b = p.get_fitness()
      file.write(f'{a}, {b}\n')

  def get_fitness_population(self):
    return [x.get_fitness() for x in self.population]

  def roulette(self): # use fitness shift
    fitness_values = self.get_fitness_population()
    offset = abs(min(fitness_values)) + 1
    adjusted = [f + offset for f in fitness_values]
    total = sum(adjusted)
    probabilities = [f / total for f in adjusted]
    parents = []
    i = 0
    while i < self.n_pop:
        random_value = random.random()
        accumulated_sum = 0
        for individual, prob in zip(self.population, probabilities):
            accumulated_sum += prob
            if accumulated_sum >= random_value:
                i += 1
                parents.append(individual)
                break

    return parents

  def tournament(self):
    parents = []
    i = 0
    while( i < self.n_pop):
      p1 = np.random.randint(0, self.n_pop)
      p2 = np.random.randint(0, self.n_pop)
      while(p1 == p2):
        p2 = np.random.randint(0, self.n_pop)
      random_victory = random.uniform(0, 1)
      fitness_p1 = self.population[p1].get_fitness()
      fitness_p2 = self.population[p2].get_fitness()
      if (fitness_p1 > fitness_p2) or (fitness_p1 < fitness_p2 and random_victory > self.prob_victory):
          winner = self.population[p1]
      else:
          winner = self.population[p2]
      parents.append(winner)
      i += 1
    return parents
  
  def get_crossing(self):
    new_generation = []
    for i in range(0, self.n_pop, 2):
        p1 = np.array(self.parents[i].get_set_items())
        p2 = np.array(self.parents[i + 1].get_set_items())
        if random.random() <= self.prob_crossing:
            point = random.randint(1, self.num_items - 1)
            offspring1 = np.concatenate([p1[:point], p2[point:]])
            offspring2 = np.concatenate([p2[:point], p1[point:]])
        else:
            offspring1, offspring2 = p1, p2
        new_generation.extend([Knapsack(self.items, offspring1, **self.kwargs), Knapsack(self.items, offspring2, **self.kwargs)])
    return new_generation

  def get_mutation(self):
    for i in range(self.n_pop):
        set_items = self.population_aux[i].get_set_items()
        mutated = False
        mutated_items = []
        new_items = np.array([
            1 - bit if random.random() <= self.prob_mutation else bit
            for bit in set_items])
        if not np.array_equal(new_items, set_items):
            mutated = True
        if mutated:
            self.population_aux[i] = copy.deepcopy(Knapsack(self.items, new_items, **self.kwargs))   
                
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
        self.population_aux = copy.deepcopy(self.get_crossing())
        self.get_mutation()
        if self.elitism:
          self.population = self.get_elitism()
        else:
          self.population = self.population_aux
        self.best_solutions = self.get_best_solutions()[:self.n_elite]
        generation += 1 
    print(self.best_solutions[0].get_set_items())
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