import numpy as np
from surfaces.surface import Surface

class Sphere(Surface):
    def __init__(self, position, radius, material_index):
        super(Sphere, self).__init__(material_index)
        self.position = np.array(position)
        self.radius = radius
    
    def __str__(self):
        return f'Sphere[position={self.position} radius={self.radius}]'

    def on_set_p0(self):
        self.p0minuspos = self.p0 - self.position
        self.c_times_4 = 4 * (np.dot(self.p0minuspos, self.p0minuspos) - self.radius * self.radius)

    def calculate_intersection_factor(self, vto) -> float:
        b = 2 * np.dot(vto, self.p0minuspos)
        delta = b ** 2 - self.c_times_4
        if delta < 0:
            return -1
        
        deltasqrt = np.sqrt(delta)
        # Find the closer intersection point
        if -b - deltasqrt < 0:
            t = (-b + np.sqrt(delta)) / 2
        else:
            t = (-b - np.sqrt(delta)) / 2

        return t