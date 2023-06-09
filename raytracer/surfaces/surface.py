from material import Material

class Surface(object):
    def __init__(self, material_index):
        self.material_index = material_index
        self.material = None

    def set_material(self, material: Material):
        self.material = material