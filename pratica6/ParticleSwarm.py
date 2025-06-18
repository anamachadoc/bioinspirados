from Particle import Particle 
from typing import Any, Dict
import os

class ParticleSwarm():
    def __init__(self, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        os.makedirs(self.output_path, exist_ok=True)