from Individual import Individual
import numpy as np
import random
import copy
import matplotlib.pyplot as plt

class GeneticAlgorithm():
  def __init__(self, **kwargs):
    for key, value in kwargs.get("GA", {}).items():
        setattr(self, key, value)
    self.config_individual = kwargs.get("Individual", {})
    self.parents = None
    self.best_fitness_per_generation = []
    self.population = [Individual(individual, **self.config_individual) 
        for individual in [
            np.random.uniform(low=self.config_individual['x_min'], high=self.config_individual['x_max'], size=(self.config_individual['n_parameters'])) 
            for _ in range(self.n_pop)]
    ]
    self.population_aux = []
    self.best_solutions = self.get_best_solutions()

  def get_best_solutions(self):
    sorted_population = sorted(self.population, key=lambda x: x.get_fitness())
    return sorted_population[:self.n_elite]

  def get_pop(self, pop, file):
    for p in pop:
      a = p.get_chromosome()
      b = p.get_fitness()
      file.write(f'{a}, {b}\n')

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
      if (fitness_p1 < fitness_p2) or (fitness_p1 > fitness_p2 and random_victory > self.prob_victory):
          winner = self.population[p1]
      else:
          winner = self.population[p2]
      parents.append(winner)
      i += 1
    return parents

  def get_crossing(self):
    new_generation = []
    for i in range(0, self.n_pop, 2):
        p1 = np.array(self.parents[i].get_chromosome())
        p2 = np.array(self.parents[i + 1].get_chromosome())
        if random.random() <= self.prob_crossing:
            point = random.randint(1, self.config_individual['n_bits'] - 1)
            offspring1 = [np.concatenate((p1[j][:point], p2[j][point:])) for j in range(2)]
            offspring2 = [np.concatenate((p2[j][:point], p1[j][point:])) for j in range(2)]
        else:
            offspring1, offspring2 = p1, p2
        new_generation.extend([Individual(offspring1, **self.config_individual), Individual(offspring2, **self.config_individual)])
    return new_generation

  def get_mutation(self):
    for i in range(self.n_pop):
        chromosome = self.population_aux[i].get_chromosome()
        mutated = False
        mutated_genes = []
        for gene in chromosome:
            new_gene = np.array([
                1 - bit if random.random() <= self.prob_mutation else bit
                for bit in gene])
            if not np.array_equal(gene, new_gene):
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
        self.parents = self.tournament() 
        self.population_aux = copy.deepcopy(self.get_crossing())
        self.get_mutation()
        self.population = self.get_elitism()
        self.best_solutions = self.get_best_solutions()
        generation += 1
    self.plot_fitness()
    self.save_fitness()

  def plot_fitness(self):
        plt.plot(self.best_fitness_per_generation)
        plt.title('Best Fitness Across Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.grid(True)
        plt.savefig('output/best_fitness.png')
        #plt.show()
        
  def save_fitness(self):
    n = self.config_individual['n_bits']
    with open(f'output/best_fitness_{n}.txt', 'w') as file:
      file.write(f'{self.best_solutions[0].get_fitness()}')