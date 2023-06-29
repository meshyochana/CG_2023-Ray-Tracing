import numpy as np
from material import Material
from surfaces.surface import Surface
from surfaces.infinite_plane import TwoParallelInfinitePlanes
from rays.ray import Ray
from light_hit import LightHit, CubeLightHit

class Cube(Surface):
    def __init__(self, position, scale, material_index):
        super(Cube, self).__init__(material_index)
        self.position = np.array(position)
        self.scale = scale
        self.d = scale / 2
        self.faces = self._create_faces()
        
    def _create_faces(self):
        # TODO: np.abs((1-I) @ position / sqrt(2))
        yz_offset = np.dot(np.array([1, 0, 0]), self.position)
        xz_offset = np.dot(np.array([0, 1, 0]), self.position)
        xy_offset = np.dot(np.array([0, 0, 1]), self.position)
        yz_planes = TwoParallelInfinitePlanes([1, 0, 0], yz_offset, self.d, self.material_index)
        xz_planes = TwoParallelInfinitePlanes([0, 1, 0], xz_offset, self.d, self.material_index)
        xy_planes = TwoParallelInfinitePlanes([0, 0, 1], xy_offset, self.d, self.material_index)
        return [yz_planes, xz_planes, xy_planes]

    """
    def on_set_p0(self):
        for corner in self.faces:
            corner.on_set_p0()
    """

    def _is_face_hit(self, hit: LightHit):
        position_without_norm = hit.position - np.multiply(hit.position, np.abs(hit.surface.normal))
        free_indexes = np.where(hit.surface.normal == 0)

        return np.max(np.abs(hit.position[free_indexes] - self.position[free_indexes])) <= self.d
    
    def intersect(self, ray: Ray) -> LightHit:
        infinite_planes_intersections = [face.intersect(ray) for face in self.faces]
        if infinite_planes_intersections[0]:
            a = 1
        faces_intersections = [CubeLightHit(self, hit.surface, hit.ray, hit.alpha) for hit in infinite_planes_intersections
                               if hit is not None and self._is_face_hit(hit)]
        if not faces_intersections:
            return None
        
        nearest_intersection = min(faces_intersections)
        # if nearest_intersection == infinite_planes_intersections[1]:
        #     a = 1
        return nearest_intersection
    
    def set_material(self, material: Material):
        super().set_material(material)
        for f in self.faces:
            f.set_material(material)

    def get_reflection_ray(self, ray: Ray, hit: CubeLightHit) -> Ray:
        """
        Get a view ray and its intersection_alpha point and return its reflection ray
        @param[in] view_ray The view ray
        @param[in] intersection_alpha The alpha where the view_ray intersects with the surface
        """
        # hit.surface is InfinitePlane
        return hit.surface.get_reflection_ray(ray, hit)
    
    def get_normal(self, hit: CubeLightHit):
        # Actually intersect with the face (InfinitePlane), doesn't matter
        # hit.surface is InfinitePlane
        return hit.surface.get_normal(hit)
    
    