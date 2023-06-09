from surfaces.surface import Surface

class InfinitePlane(Surface):
    def __init__(self, normal, offset, material_index):
        super(InfinitePlane, self).__init__(material_index)
        self.normal = normal
        self.offset = offset
