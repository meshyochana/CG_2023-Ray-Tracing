import numpy as np
from material import Material
from surfaces.surface import Surface
from light_hit import LightHit

EPSILON = 0.000001

class InfinitePlane(Surface):
    def __init__(self, normal, offset, material_index):
        super(InfinitePlane, self).__init__(material_index)
        self.normal = np.array(normal)
        self.normal = self.normal / np.linalg.norm(self.normal)
        self.offset = np.array(offset) # XXX: Reverse than configuration
        self.p0normaldotplusoffset = None

    """
    def on_set_p0(self):
        self.p0normaldotplusoffset = -np.dot(self.p0, self.normal) + self.offset
    """

    def intersect(self, ray) -> LightHit:
        # XXX: Should we take abs? or reverse the normal if negative?
        minusp0normaldotplusoffset = -(np.dot(ray.p, self.normal) - self.offset)
        if minusp0normaldotplusoffset > 0:
            return None
        dot_result = np.dot(ray.vto, self.normal)
        if not dot_result:
            return None
        
        t = minusp0normaldotplusoffset / dot_result
        if t < 0:
            return None
        hit = LightHit(self, ray, t)
        return hit
        # p = self.p0 + t * vto
        # return p

    def __str__(self):
        return f'InfinitePlane[normal={self.normal} offset={self.offset}]'
    
    def get_normal(self, hit):
        return self.normal


class TwoParallelInfinitePlanes(Surface):
    def __init__(self, normal, offset, d, material_index):
        super(TwoParallelInfinitePlanes, self).__init__(material_index)
        self.plane1 = InfinitePlane([-n for n in normal], offset - d, material_index)
        self.plane2 = InfinitePlane(normal, offset + d, material_index)
    """
    def on_set_p0(self):
        self.p0normaldot1 = -np.dot(self.p0, self.normal) + self.offset1
        self.p0normaldot2 = -np.dot(self.p0, self.normal) + self.offset2
    """
    def set_material(self, material: Material):
        super().set_material(material)
        self.plane1.set_material(material)
        self.plane2.set_material(material)

    def intersect(self, ray) -> LightHit:
        hit1 = self.plane1.intersect(ray)
        hit2 = self.plane2.intersect(ray)
        if hit1 is None:
            if hit2 is not None:
                a = 1
            return hit2
        if hit2 is None:
            return hit1
        return min([hit1, hit2])
    
    def get_normal(self, hit):
        for twofaces in hit.faces:
            if self.plane1 in twofaces:
                return self.plane1.get_normal()
            elif self.plane2 in hit.faces:
                return self.plane2.get_normal()
        else:
            raise Exception('No plane is on hit surfaces')
    