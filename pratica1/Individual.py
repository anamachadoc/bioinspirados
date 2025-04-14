import math
from typing import Any, Dict, List

class Individual():
  def __init__(self, parameters: List[List], **kwargs: dict[str, Any]):
    for key, value in kwargs.items():
        setattr(self, key, value)
    self.chromosome = parameters
    self.fitness = self.function_fitness()

  def get_chromosome(self):
    return self.chromosome

  def get_decode_parameter(self, parameter):
    x = sum(2**(self.n_bits - 1 - i ) * value for i, value in enumerate(parameter))
    return self.x_min + (self.x_max - self.x_min)/(pow(2, self.n_bits) - 1) * x

  def function_fitness(self):
    return -20 * pow(math.e, (-0.2 * math.sqrt(1/self.n_parameters * sum(self.get_decode_parameter(x)**2 for x in self.chromosome)))) - pow(math.e, 1/self.n_parameters * sum(math.cos(2 * math.pi * self.get_decode_parameter(x)) for x in self.chromosome)) + 20 + math.e

  def get_fitness(self):
    return self.fitness