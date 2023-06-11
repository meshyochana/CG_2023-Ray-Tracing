from material import Material
from light_hit import LightHit

class Surface(object):
    def __init__(self, material_index):
        self.material_index = material_index
        self.material = None
        self.p0 = None

    def set_p0(self, p0):
        self.p0 = p0
        self.on_set_p0()

    def on_set_p0(self):
        pass

    def set_material(self, material: Material):
        self.material = material

    def calculate_intersection_factor(self, vto) ->float:
        """
        Check whether a ray intersects with the object, and if so, calculate the intersection distance
        @param[in] vto: The direction of the ray

        @return The factor alpha thus the intersection points equals p0 + alpha * vto.
                If there is no intersection, the returned factor will be negative
        """
        return -1
    
    def get_intersection(self, vto):
        alpha = self.calculate_intersection_factor(vto)
        hit = LightHit(self, alpha)
        return hit
