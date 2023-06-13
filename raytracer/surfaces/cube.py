import numpy as np
from surfaces.surface import Surface
from surfaces.infinite_plane import TwoParallelInfinitePlanes

class Cube(Surface):
    def __init__(self, position, scale, material_index):
        super(Cube, self).__init__(material_index)
        self.position = position
        self.scale = scale
        self.d = scale // 2
        self.corners = self._create_corners()
        
    def _create_corners(self):
        x_distance = self.position[1] * self.position[2]
        y_distance = self.position[0] * self.position[2]
        z_distance = self.position[0] * self.position[1]
        yz_planes = TwoParallelInfinitePlanes([1, 0, 0], x_distance - self.d, x_distance + self.d)
        xz_planes = TwoParallelInfinitePlanes([0, 1, 0], y_distance - self.d, y_distance + self.d)
        xy_planes = TwoParallelInfinitePlanes([0, 0, 1], z_distance - self.d, z_distance + self.d)
        return [yz_planes, xz_planes, xy_planes]

    def on_set_p0(self):
        for corner in self.corners:
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