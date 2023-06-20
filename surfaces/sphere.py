import numpy as np
from surfaces.surface import Surface
from rays.reflection_ray import ReflectionRay
from rays.view_ray import ViewRay

class Sphere(Surface):
    def __init__(self, position, radius, material_index):
        super(Sphere, self).__init__(material_index)
        self.position = np.array(position)
        self.radius = radius
        self.r_square = radius ** 2
    
    def __str__(self):
        return f'Sphere[position={self.position} radius={self.radius}]'

    def on_set_p0(self):
        self.L = self.position - self.p0
        self.r_square_minus_L_square = self.r_square - np.dot(self.L, self.L)

    def calculate_intersection_factor(self, view_ray: ViewRay) -> float:
        # Implement using geometric method
        t_ca = np.dot(self.L, view_ray.vto)
        if t_ca < 0:
            return -1
        t_hc_square = self.r_square_minus_L_square + t_ca ** 2
        if t_hc_square < 0:    
            # print('awwww snap 2')
            return -1
        
        t_hc = np.sqrt(t_hc_square)
        t1 = t_ca - t_hc
        t2 = t_ca + t_hc
        if t1 < 0 and t2 < 0:
            print('awwww snap 3')
            return -1
        # print(f't1={t1}, t2={t2}')
        return t1
    
    def get_reflection_ray(self, view_ray: ViewRay, intersection: np.array) -> ReflectionRay:
        # intersection_point = view_ray.p + intersection_alpha * view_ray.vto
        radius = intersection - self.position
        norm = radius / np.linalg.norm(radius)
        norm_component = np.dot(norm, view_ray)
        reflection_ray_direction = ReflectionRay(intersection, view_ray.vto + 2 * norm_component)
        return reflection_ray_direction

    def get_normal(self, point):
        mid_result = point - self.position
        result = mid_result / np.linalg.norm(mid_result)
        return result