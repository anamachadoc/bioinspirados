import math
from typing import Any, Dict, List
from Item import Item 

class Knapsack():
  def __init__(self, items: List[Item], set_items: List[int], **kwargs: dict[str, Any]):
    for key, value in kwargs.items():
        setattr(self, key, value)
    self.items = items
    self.capacity =self.get_capacity()
    self.set_items = set_items
    self.position_items = [idx for idx, binary_item in enumerate(self.set_items) if binary_item]
    self.weight = sum([self.items[p].get_weight() for p in self.position_items])
    self.fitness = self.function_fitness()

  def get_capacity(self):
    with open(self.path_c, 'r') as file: return int(file.readline().strip())
  
  def get_position_items(self):
    return self.position_items
  
  def get_knapsack_items(self):
    for p in self.position_items:
      self.items[p].get_item()
      
  def get_weight(self):
    return self.weight

  def get_fitness(self):
    return self.fitness
  
  def get_set_items(self):
    return self.set_items
    
  def function_fitness(self):
    return (
        self.function_fitness_without_penalty()
        if self.weight <= self.capacity
        else self.function_fitness_second_penalty())

  def function_fitness_without_penalty(self):
    return sum([self.items[p].get_utility_value() for p in self.position_items])
  
  def function_fitness_first_penalty(self):
    total_utility = self.function_fitness_without_penalty()
    excess_weight = sum(self.items[p].get_weight() for p in self.position_items) - self.capacity
    penalty = excess_weight / self.capacity
    return total_utility * (1 - penalty)
    
  def function_fitness_second_penalty(self):
    total_utility = self.function_fitness_without_penalty()
    excess_weight = sum(self.items[p].get_weight() for p in self.position_items) - self.capacity
    penalty = total_utility * excess_weight
    return total_utility - penalty
