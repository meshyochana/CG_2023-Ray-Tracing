import numpy as np

class Ray(object):
    def __init__(self, p, vto, ttl=3):
        self.p = p
        self._vto = vto / np.linalg.norm(vto)
        self.ttl = ttl

    def at(self, alpha):
        return self.p + alpha * self.vto
    
    def __str__(self):
        return f'[Ray: source {self.p} direction {self.vto}]'
    
    @property
    def vto(self):
        return self._vto


class IntersectionRay(Ray):
    def __init__(self, p, vto, ttl):
        super(IntersectionRay, self).__init__(p, vto, ttl)


class ReflectionRay(Ray):
    def __init__(self, p, vto, ttl):
        super(ReflectionRay, self).__init__(p, vto, ttl)
