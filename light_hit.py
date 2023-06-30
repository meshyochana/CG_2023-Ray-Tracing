import numpy as np

from surfaces.surface import Surface
from rays.ray import Ray
from rays.reflection_ray import ReflectionRay

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
    def __init__(self, cube: Surface, faces_hits: list, ray: Ray, alpha: float):
        super(CubeLightHit, self).__init__(cube, ray, alpha)
        self.faces_hits = faces_hits

    # def get_normal(self):
    #     normal = np.sum([face.get_normal(self) for face in self.faces])
    #     norm = np.linalg.norm(normal)
    #     if norm:
    #         normal /= norm

    #     return normal
    
    # def get_reflection_ray(self):
    #     norm = self.get_normal()
    #     norm_factor = np.dot(norm, self.ray.vto)
    #     norm_direction = self.ray.vto - 2 * norm_factor * norm
    #     reflection_ray_direction = ReflectionRay(self.position, norm_direction, self.ray.ttl - 1)
    #     return reflection_ray_direction
