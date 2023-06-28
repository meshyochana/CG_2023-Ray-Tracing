import numpy as np
from surfaces.surface import Surface
from rays.reflection_ray import ReflectionRay
from rays.ray import Ray
from light_hit import LightHit

class Sphere(Surface):
    def __init__(self, position, radius, material_index):
        super(Sphere, self).__init__(material_index)
        self.position = np.array(position)
        self.radius = radius
        self.r_square = radius ** 2
    
    def __str__(self):
        return f'Sphere[position={self.position} radius={self.radius}]'
    
    """
    def on_set_p0(self):
        self.L = self.position - self.p0
        self.r_square_minus_L_square = self.r_square - np.dot(self.L, self.L)
    """

    def intersect(self, ray: Ray) -> LightHit:
        # Implement using geometric method
        L = self.position - ray.p
        r_square_minus_L_square = self.r_square - np.dot(L, L)
        t_ca = np.dot(L, ray.vto)
        if t_ca < 0:
            return None
        t_hc_square = r_square_minus_L_square + t_ca ** 2
        if t_hc_square < 0:    
            # print('awwww snap 2')
            return None
        
        t_hc = np.sqrt(t_hc_square)
        t1 = t_ca - t_hc
        t2 = t_ca + t_hc
        if t1 < 0 and t2 < 0:
            print('awwww snap 3')
            return None
        # print(f't1={t1}, t2={t2}')
        hit = LightHit(self, ray, t1)
        return hit

    def get_normal(self, hit: LightHit):
        mid_result = hit.position - self.position
        result = mid_result / np.linalg.norm(mid_result)
        return result