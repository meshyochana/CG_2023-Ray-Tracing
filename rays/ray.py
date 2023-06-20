import numpy as np

class Ray(object):
    def __init__(self, p, vto, ttl=10):
        self.p = p
        self.vto = vto / np.linalg.norm(vto)
        self.ttl = ttl

    def at(self, alpha):
        return self.p + alpha * self.vto