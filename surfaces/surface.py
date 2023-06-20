from material import Material
from rays.view_ray import ViewRay
from rays.reflection_ray import ReflectionRay

class Surface(object):
    def __init__(self, material_index):
        self.material_index = material_index - 1 # Given from 1, we want from 0
        self.material = None
        self.p0 = None

    def set_p0(self, p0):
        self.p0 = p0
        self.on_set_p0()

    def on_set_p0(self):
        pass

    def set_material(self, material: Material):
        self.material = material

    def calculate_intersection_factor(self, view_ray: ViewRay) ->float:
        """
        Check whether a ray intersects with the object, and if so, calculate the intersection distance
        @param[in] vto The direction of the ray

        @return The factor alpha thus the intersection points equals p0 + alpha * vto.
                If there is no intersection, the returned factor will be negative
        """
        return -1
    
    def get_reflection_ray(self, view_ray: ViewRay, intersection_alpha: float) -> ReflectionRay:
        """
        Get a view ray and its intersection_alpha point and return its reflection ray
        @param[in] view_ray The view ray
        @param[in] intersection_alpha The alpha where the view_ray intersects with the surface
        """
        raise NotImplementedError()
    
    def get_normal(self, point):
        raise NotImplementedError()
    