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
    
    def __eq__(self, other):
        if other is None or not isinstance(other, LightHit):
            return False
        return self.surface == other.surface and self.alpha == other.alpha and self.ray == other.ray
    
    def get_normal(self):
        normal = self.surface.get_normal(self)
        return normal
    
    def get_reflection_ray(self):
        reflection = self.surface.get_reflection_ray(self.ray, self)
        return reflection
    
    def __str__(self):
        return f'Hit! Ray {self.ray} at {self.position} (alpha {self.alpha}) hit {self.surface}'
    
    def __repr__(self):
        return self.__str__()

class CubeLightHit(LightHit):
    def __init__(self, cube: Surface, face: Surface, ray: Ray, alpha: float):
        super(CubeLightHit, self).__init__(face, ray, alpha)
        self.cube = cube

    def get_normal(self):
        normal = self.surface.get_normal(self)
        return normal
    
    def get_reflection_ray(self):
        reflection = self.surface.get_reflection_ray(self.ray, self)
        return reflection
    
