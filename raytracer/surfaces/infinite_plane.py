import numpy as np
from surfaces.surface import Surface

class InfinitePlane(Surface):
    def __init__(self, normal, offset, material_index):
        super(InfinitePlane, self).__init__(material_index)
        self.normal = np.array(normal)
        self.offset = np.array(offset)
        self.p0normaldotplusoffset = None

    def on_set_p0(self):
        self.p0normaldot = -np.dot(self.p0, self.normal) + self.offset

    def calculate_intersection_factor(self, vto) -> float:
        t = self.p0normaldotplusoffset / np.dot(vto, self.normal)
        p = self.p0 + t * vto
        return p
