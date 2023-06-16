import numpy as np
from surfaces.surface import Surface
from surfaces.infinite_plane import TwoParallelInfinitePlanes

class Cube(Surface):
    def __init__(self, position, scale, material_index):
        super(Cube, self).__init__(material_index)
        self.position = position
        self.scale = scale
        self.d = scale // 2
        self.faces = self._create_faces()
        
    def _create_faces(self):
        # TODO: np.abs((1-I) @ position / sqrt(2))
        yz_distance = np.abs(np.dot(np.array([0, 1, 1]) / np.sqrt(2), self.position))
        xz_distance = np.abs(np.dot(np.array([1, 0, 1]) / np.sqrt(2), self.position))
        xy_distance = np.abs(np.dot(np.array([1, 1, 0]) / np.sqrt(2), self.position))
        yz_planes = TwoParallelInfinitePlanes([1, 0, 0], yz_distance - self.d, yz_distance + self.d)
        xz_planes = TwoParallelInfinitePlanes([0, 1, 0], xz_distance - self.d, xz_distance + self.d)
        xy_planes = TwoParallelInfinitePlanes([0, 0, 1], xy_distance - self.d, xy_distance + self.d)
        return [yz_planes, xz_planes, xy_planes]

    def on_set_p0(self):
        for corner in self.faces:
            corner.on_set_p0()
    
    def calculate_intersection_factor(self, vto):
        alphas = np.array([plane.calculate_intersection_factor(vto) for plane in self.planes])
        intersections = self.p0 + np.array([self.p0 + alpha * vto for alpha in alphas])
        # TODO: Move to numpy
        relevant_intersections = list()
        for i in len(intersections):
            distance_from_middle = intersections[i] -self.p0
            if np.max(np.abs(distance_from_middle)) <= self.d:
                relevant_intersections.append(i)

        if not relevant_intersections:
            nearest_intersection = -1
        else:
            nearest_intersection = min(relevant_intersections, key=lambda i: alphas[i])

        return nearest_intersection