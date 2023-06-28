import numpy as np
from material import Material
from rays.ray import Ray
from rays.reflection_ray import ReflectionRay

class Surface(object):
    def __init__(self, material_index):
        self.material_index = material_index - 1 # Given from 1, we want from 0
        self.material = None
        self.p0 = None

    """
    def set_p0(self, p0):
        self.p0 = p0
        self.on_set_p0()

    def on_set_p0(self):
        pass
    """

    def set_material(self, material: Material):
        self.material = material

    def intersect(self, ray: Ray):
        """
        Check whether a ray intersects with the object, and if so, calculate the intersection distance
        @param[in] vto The direction of the ray

        @return The LightHit object of the nearest intersection with the plane, or None if not intersects
        """
        raise NotImplementedError()
    
    def get_reflection_ray(self, ray: Ray, intersection) -> ReflectionRay:
        """
        Get a view ray and its intersection_alpha point and return its reflection ray
        @param[in] view_ray The view ray
        @param[in] intersection The alpha where the view_ray intersects with the surface
        """
        norm = self.get_normal(intersection)
        norm_factor = np.dot(norm, ray.vto)
        norm_direction = ray.vto - 2 * norm_factor * norm
        reflection_ray_direction = ReflectionRay(intersection.position, norm_direction, ray.ttl - 1)
        return reflection_ray_direction
    
    def get_normal(self, hit):
        raise NotImplementedError()
    
    