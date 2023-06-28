import numpy as np
from surfaces.surface import Surface
from rays.ray import Ray

class InfinitePlane(Surface):
    def __init__(self, normal, offset, material_index):
        super(InfinitePlane, self).__init__(material_index)
        self.normal = np.array(normal)
        self.normal = self.normal / np.linalg.norm(self.normal)
        self.offset = np.array(offset)
        self.p0normaldotplusoffset = None

    def on_set_p0(self):
        self.p0normaldotplusoffset = -np.dot(self.p0, self.normal) + self.offset

    def calculate_intersection_factor(self, ray : Ray) -> float:
        # XXX: Should we take abs? or reverse the normal if negative?
        t = np.abs(self.p0normaldotplusoffset / np.dot(ray.vto, self.normal))
        return t
        # p = self.p0 + t * vto
        # return p

    def __str__(self):
        return f'InfinitePlane[normal={self.normal} offset={self.offset}]'
    
    def get_normal(self, point):
        return self.normal



class TwoParallelInfinitePlanes(Surface):
    def __init__(self, normal, offset1, offset2, material_index):
        super(TwoParallelInfinitePlanes, self).__init__(material_index)
        self.normal = np.array(normal)
        self.offset1 = np.array(offset1)
        self.offset2 = np.array(offset2)
        self.p0normaldotplusoffset = None

    def on_set_p0(self):
        self.p0normaldot1 = -np.dot(self.p0, self.normal) + self.offset1
        self.p0normaldot2 = -np.dot(self.p0, self.normal) + self.offset2

    def calculate_intersection_factor(self, vto) -> float:
        vto_norm = np.dot(vto, self.normal)
        t1 = self.p0normaldotplusoffset1 / vto_norm
        t2 = self.p0normaldotplusoffset2 / vto_norm
        p1 = self.p0 + t1 * vto
        p2 = self.p0 + t2 * vto
        if p2 < p1:
            p1, p2 = p2, p1
        # TODO: Return LightHit instead, p1 is in p2 is out
        return p1
    