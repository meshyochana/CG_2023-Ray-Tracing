from surfaces.surface import Surface

class Cube(Surface):
    def __init__(self, position, scale, material_index):
        super(Cube, self).__init__(material_index)
        self.position = position
        self.scale = scale

    def on_set_p0(self):
        # TODO
        pass
    
    def calculate_intersection_factor(self, vto):
        # TODO
        raise NotImplementedError()