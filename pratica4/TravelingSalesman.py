from Path import Path 
from typing import Any, Dict
import random
import matplotlib.pyplot as plt
import copy
import numpy as np

class TravelingSalesman():
  def __init__(self, **kwargs: Dict[str, Any]):
    for key, value in kwargs.items():
      setattr(self, key, value)
    self.cities = list(range(1, self.num_cities + 1))
    self.set_paths = [Path(path + [path[0]], self.distance_cities, self.coordenates_cities)
        for path in ( random.sample(self.cities, self.num_cities) for _ in range(self.n_pop))]
    print('POPULAÇÃO INICIAL')
    self.print_pop(self.set_paths)
    self.path_aux = []
    self.best_solutions = self.get_best_solutions()[:2]
    self.best_fitness_per_generation = []
    self.selection_methods = {
      'tournament': self.tournament,
      'roulette': self.roulette}
      
  def get_set_paths(self):
    return self.set_paths
  
  def print_pop(self, pop):
    for p in pop:
      print(p.get_ordered_cities(), p.get_distance())
      
  def get_best_solutions(self):
    sorted_paths = sorted(self.set_paths, key=lambda x: x.get_distance())
    return sorted_paths
  
  def get_elitism(self):
    best_individuals = self.best_solutions
    position = random.sample(range(self.n_pop), k=len(best_individuals))
    #print('POSIÇÕES: ', position)
    for i, elite in enumerate(best_individuals):
        self.path_aux[position[i]] = copy.deepcopy(elite)
    return self.path_aux

  def get_crossing(self):
    def preencher(base, fixo):
        return [x for x in base if x not in fixo]

    new_generation = []

    for i in range(0, self.n_pop, 2):
        parent1 = self.set_paths[i].get_ordered_cities()
        parent2 = self.set_paths[i+1].get_ordered_cities()
        if random.random() <= self.prob_crossing:
            p1, p2 = sorted(random.sample(range(self.num_cities), 2))
            segment1 = parent1[p1:p2]
            segment2 = parent2[p1:p2]
            rest1 = preencher(parent2, segment1)
            rest2 = preencher(parent1, segment2)
            child1 = rest1[:p1] + segment1 + rest1[p1:]
            child2 = rest2[:p1] + segment2 + rest2[p1:]
        else:
            child1 = parent1
            child2 = parent2
        new_generation.append(Path(child1 + [child1[0]], self.distance_cities, self.coordenates_cities))
        new_generation.append(Path(child2 + [child2[0]], self.distance_cities, self.coordenates_cities))

    return new_generation

  def get_mutation(self):
    for i in range(self.n_pop):
        path = self.path_aux[i].get_ordered_cities()
        mutated = False
        for j in range(self.num_cities):
            if random.random() <= self.prob_mutation:
              p1 = random.randint(0, self.num_cities - 1)
              while (p1 == j):
                p1 = random.randint(0, self.num_cities - 1)
              path[j], path[p1] = path[p1], path[j]
              mutated = True
        if mutated:
            self.path_aux[i] = copy.deepcopy(Path(path + [path[0]], self.distance_cities, self.coordenates_cities))
     
  def roulette(self):
    parents = []
    sum_distance = sum([p.get_inverted_distance(self.inversion_constant) for p in self.set_paths])
    roulette_values = [p.get_inverted_distance(self.inversion_constant)/sum_distance for p in self.set_paths]
    i = 0
    while( i < self.n_pop):
      random_value = random.random()
      accumulated_sum = 0
      for j, prob in enumerate(roulette_values):  
          accumulated_sum += prob
          if accumulated_sum >= random_value:
              parents.append(self.set_paths[j])
              i = i + 1
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
      distance_p1 = self.set_paths[p1].get_distance()
      distance_p2 = self.set_paths[p2].get_distance()
      if (distance_p1 < distance_p2) or (distance_p1 >= distance_p2 and random_victory > self.prob_victory):
          winner = self.set_paths[p1]
      else:
          winner = self.set_paths[p2]
      parents.append(winner)
      i += 1
    return parents
  
  def run(self):
    generation = 0
    while generation < self.n_gen:
        self.best_fitness_per_generation.append(self.best_solutions[0].get_distance())
        print(f"Geração {generation}: {self.best_solutions[0].get_distance()}")
        #print('ESCOLHA DOS PAIS')
        self.parents = self.selection_methods.get(self.select_by, self.roulette)()
        #self.print_pop(self.parents)
        self.set_paths = self.parents
        #print('NOVA GERAÇÃO')
        self.path_aux = self.get_crossing()
        #self.print_pop(self.path_aux)
        #print('MUTAÇÃO')
        self.get_mutation()
        #self.print_pop(self.path_aux)
        #print('ELITISMO')
        self.set_paths = self.get_elitism()
        #self.print_pop(self.set_paths)
        self.best_solutions = self.get_best_solutions()[:2]
        #print('MELHOR SOLUÇÃO')
        #print(self.best_solutions[0].get_ordered_cities(), self.best_solutions[0].get_distance())
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
    with open(f'output/best_fitness.txt', 'w') as file:
      file.write(f'{self.best_solutions[0].get_ordered_cities()}')
      file.write(f'{self.best_solutions[0].get_distance()}')
    
  