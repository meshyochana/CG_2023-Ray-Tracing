import numpy as np
from material import Material
from surfaces.surface import Surface
from surfaces.infinite_plane import TwoParallelInfinitePlanes
from rays.ray import Ray
from rays.reflection_ray import ReflectionRay
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

    def _is_cube_hit(self, faces_hits: list[LightHit]):
        if not faces_hits:
            return False
        relevant_components = np.array([face_hit.surface.normal == 0 for face_hit in faces_hits])
        free_indexes = np.where(np.all(relevant_components == True, axis=0))[0]
        max_diff = np.max(np.abs(faces_hits[0].position[free_indexes] - self.position[free_indexes]))
        is_hit = max_diff <= self.d
        if is_hit:
            a = 1
        return is_hit
    
    def intersect(self, ray: Ray) -> LightHit:
        infinite_planes_intersections = [twofaces.intersect(ray) for twofaces in self.faces]

        # Create a dictionary from alpha to all the faces with that alpha value        
        alphas_to_faces_hits = dict()
        for p in infinite_planes_intersections:
            if p is not None:
                alphas_to_faces_hits.setdefault(p.alpha, list()).append(p)
        
        faces_intersections = [CubeLightHit(self, faces, ray, alpha) for alpha, faces in alphas_to_faces_hits.items()
                               if self._is_cube_hit(faces)]
        
        if not faces_intersections:
            return None
        
        nearest_intersection = min(faces_intersections)
        # if nearest_intersection == infinite_planes_intersections[1]:
        #     a = 1
        # if np.all(np.array([0,1,0] != nearest_intersection.surface.normal)):
            # print(f'nearest intersection norm: {nearest_intersection.surface.normal}')
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
        norm = self.get_normal(hit)
        norm_factor = np.dot(norm, ray.vto)
        norm_direction = ray.vto - 2 * norm_factor * norm
        reflection_ray_direction = ReflectionRay(self.position, norm_direction, ray.ttl - 1)
        return reflection_ray_direction
    
    def get_normal(self, hit: CubeLightHit):
        # Actually intersect with the face (InfinitePlane), doesn't matter
        # hit.surface is InfinitePlane
        normal = sum([face_hit.get_normal() for face_hit in hit.faces_hits])
        norm = np.linalg.norm(normal)
        if norm:
            normal /= norm

        return normal
    
    