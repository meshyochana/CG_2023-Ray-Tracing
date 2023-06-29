import numpy as np

from rays.ray import Ray
from light import Light


class LightRay(Ray):
    def __init__(self, light: Light, position: np.array):
        hit_to_light = position - light.position
        super(LightRay, self).__init__(light.position, hit_to_light)

    # @property
    # def vto(self):
        # return -self._vto
    