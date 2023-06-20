import numpy as np

from light_hit import LightHit

class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, radius):
        self.position = np.array(position)
        self.color = np.array(color)
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.radius = radius

    def get_intensity(self, point: np.array):
        return 1
        # TODO: Implement soft shadows here
        vec_d = self.position - point
        d_square = np.dot(vec_d, vec_d)
        return self.specular_intensity / d_square
    

    # def diffuse_coeffecient(self, hit: LightHit):
    #     d = np.abs(self.position - hit.position)
    #     kc = 
    #     kl =
    #     kq =
    #     intensity = self.specular_intensity / (kc + kl * d + kq * (d ** 2)