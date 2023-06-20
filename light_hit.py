import numpy as np

from surfaces.surface import Surface
from rays.ray import Ray

class LightHit:
    def __init__(self, surface: Surface, ray: Ray, alpha: float):
        self.surface = surface
        self.alpha = alpha
        self.ray = ray
        self.position = ray.at(alpha)

    def __lt__(self, other):
        return self.alpha < other.alpha
    
    def get_normal(self):
        normal = self.surface.get_normal(self.position)
        return normal
    
    def get_reflection_ray(self):
        reflection = self.surface.get_reflection_ray(self.ray, self.position)
        return reflection
    
    def __str__(self):
        return f'Hit! Ray {self.ray} at {self.position} (alpha {self.alpha}) hit {self.surface}'
    
    def __repr__(self):
        return self.__str__()