import numpy as np

from surfaces.surface import Surface
from rays.ray import Ray

class LightHit:
    def __init__(self, surface: Surface, ray: Ray, alpha: float):
        self.surface = surface
        self.alpha = alpha
        self.position = ray.at(alpha)

    def __lt__(self, other):
        return self.alpha < other.alpha
    
    def get_normal(self):
        normal = self.surface.get_normal(self.position)
        return normal