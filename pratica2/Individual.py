import math
from typing import Any, Dict, List

class Individual():
  def __init__(self, parameters: List[float], **kwargs: dict[str, Any]):
    for key, value in kwargs.items():
        setattr(self, key, value)
    self.chromosome = parameters
    self.fitness = self.function_fitness()

  def get_chromosome(self):
    return self.chromosome
  
  def get_inverted_fitness(self):
    return 1/(self.fitness + self.inversion_constant)

  def function_fitness(self):
    return -20 * pow(math.e, (-0.2 * math.sqrt(1/self.n_parameters * sum(x**2 for x in self.chromosome)))) - pow(math.e, 1/self.n_parameters * sum(math.cos(2 * math.pi * x) for x in self.chromosome)) + 20 + math.e

  def get_fitness(self):
    return self.fitness