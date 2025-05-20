from Path import Path 
from typing import Any, Dict, List

class TravelingSalesman():
  def __init__(self, set_paths: List[Path], **kwargs: Dict[str, Any]):
    for key, value in kwargs.items():
        setattr(self, key, value)
    self.set_paths = set_paths