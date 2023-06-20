import numpy as np
from rays.ray import Ray

class ViewRay(Ray):
    def vto_dot_norm(self, n):
        return np.dot(n, self.vto)
    