from AntColony import AntColony
import yaml
import sys

def get_infos(path):
    
    distance = {}
    row_index = 1  
    with open(f'{path}_dist.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            numbers = list(map(int, line.split()))
            distance[row_index] = {}
            for col_index, num in enumerate(numbers, start=1): 
                distance[row_index][col_index] = num
            row_index += 1
            
    with open(f'{path}_xy.txt', 'r') as f:
        lines = f.readlines()
    xy = {}
    for i, line in enumerate(lines, start=1):
        if line.strip():
            coords = line.split()
            x = float(coords[0])
            y = float(coords[1])
            xy[i] = (x, y)

    return distance, xy

if __name__ == "__main__":
    with open('config_temp.yaml', 'r') as file:
        kwargs = yaml.safe_load(file)   
    kwargs['distance_cities'], kwargs['coordenates_cities'] = get_infos(kwargs['input_path'])
    kwargs['possible_cities'] = list(kwargs['distance_cities'].keys())
    kwargs['output_path'] = sys.argv[1]
    AC = AntColony(**kwargs)
    AC.run()
