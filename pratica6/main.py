from ParticleSwarm import ParticleSwarm
import yaml
import sys

if __name__ == "__main__":
    with open('config_temp.yaml', 'r') as file:
        kwargs = yaml.safe_load(file)   
    kwargs['output_path'] = sys.argv[1]
    
p = ParticleSwarm(**kwargs)
p.run()