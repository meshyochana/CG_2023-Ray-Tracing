import numpy as np

class Ray(object):
    def __init__(self, p, vto, ttl=10):
        self.p = p
        self.vto = vto / np.linalg.norm(vto)
        self.ttl = ttl

    def at(self, alpha):
        return self.p + alpha * self.vto
    
    def vto_dot_norm(self, n):
        raise NotImplementedError()
    
    def __str__(self):
        return f'[Ray: source {self.p} direction {self.vto}]'