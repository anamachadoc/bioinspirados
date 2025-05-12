import math
from typing import Any, Dict, List
from pratica3.Knapsack import Item 

class Knapsack():
  def __init__(self, parameters: List[Item], **kwargs: dict[str, Any]):
    for key, value in kwargs.items():
        setattr(self, key, value)
    self.itens = parameters
    self.fitness = self.function_fitness()

  def get_chromosome(self):
    return self.chromosome
  
  def function_fitness_without_penalty(self):
    pass
  
  def function_fitness_first_penalty(self):
    pass
  
  def function_fitness_second_penalty(self):
    pass
  
  def get_fitness(self):
    return self.fitness