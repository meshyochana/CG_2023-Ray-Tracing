import numpy as np

from rays.ray import Ray
from light import Light


class LightRay(Ray):
    def __init__(self, light: Light, position: np.array):
        hit_to_light = light.position - position
        super(LightRay, self).__init__(position, hit_to_light)

    def vto_dot_norm(self, n):
        return np.dot(n, -self.vto)