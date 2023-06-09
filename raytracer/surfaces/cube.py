from surfaces.surface import Surface

class Cube(Surface):
    def __init__(self, position, scale, material_index):
        super(Cube, self).__init__(material_index)
        self.position = position
        self.scale = scale
