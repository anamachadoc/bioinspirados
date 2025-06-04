from typing import Any, Dict, List, Tuple
import plotly.graph_objects as go

class Path():
    def __init__(self, items: List[int], distance_cities: Dict[int, Dict[int, float]], coordenates_cities: Dict[int, Tuple[int, int]]):
        self.ordered_cities = items # add fisrt city to end of list
        self.distance_cities = distance_cities
        self.distance = self.calculate_distance()
        self.coordenates_cities = coordenates_cities

    def get_distance(self):
        return self.distance
    
    def get_inverted_distance(self, inversion_constant):
        return 1/(self.distance + inversion_constant)
    
    def get_ordered_cities(self):
        return self.ordered_cities[:-1]

    def calculate_distance(self):
        distance = 0
        for i in range(len(self.ordered_cities) - 1):
            origin_city = self.ordered_cities[i]
            destination_city = self.ordered_cities[i + 1]
            distance += self.distance_cities[origin_city][destination_city]
        return distance
    
    def plot_path(self, save_path):
        fig = go.Figure()
        for city_id, (x, y) in self.coordenates_cities.items():
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                text=[str(city_id)],
                textposition='top center',
                marker=dict(size=12)
            ))

        for i in range(len(self.ordered_cities) - 1):
            x0, y0 = self.coordenates_cities[self.ordered_cities[i]]
            x1, y1 = self.coordenates_cities[self.ordered_cities[i + 1]]
            fig.add_annotation(
                ax=x0, ay=y0,
                x=x1, y=y1,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=5,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='black'
            )

        x0, y0 = self.coordenates_cities[self.ordered_cities[-1]]
        x1, y1 = self.coordenates_cities[self.ordered_cities[0]]
        fig.add_annotation(
            ax=x0, ay=y0,
            x=x1, y=y1,
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='red'
        )

        fig.update_layout(
            title='Rota entre cidades',
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            width=600,
            height=600
        )

        fig.write_image(f"{save_path}/path.png")

