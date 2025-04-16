from GA import GeneticAlgorithm
import yaml
from random import seed
import numpy as np

if __name__ == "__main__":
    seed(10)
    np.random.seed(10)
    
    with open('config.yaml', 'r') as file:
        kwargs = yaml.safe_load(file)
    
    GA = GeneticAlgorithm(**kwargs)
    GA.run()