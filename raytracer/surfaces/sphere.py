from surfaces.surface import Surface

class Sphere(Surface):
    def __init__(self, position, radius, material_index):
        super(Sphere, self).__init__(material_index)
        self.position = position
        self.radius = radius
