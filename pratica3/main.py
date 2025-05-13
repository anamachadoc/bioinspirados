from GA import GeneticAlgorithm
import yaml
import sys

if __name__ == "__main__":
    with open('config_temp.yaml', 'r') as file:
        kwargs = yaml.safe_load(file)
    
    save_path = sys.argv[1]
    GA = GeneticAlgorithm(save_path, **kwargs)
    GA.run()