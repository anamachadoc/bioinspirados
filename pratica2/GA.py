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
    self.parents = self.roulette()
    new_generation = []
    for i in range(0, self.n_pop, 2):
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