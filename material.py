class Material:
    def __init__(self, diffuse_color, specular_color, reflection_color, shininess, transparency):
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.reflection_color = reflection_color
        self.shininess = shininess
        self.transparency = transparency
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f'Material[diff_col={self.diffuse_color}, spec_col={self.specular_color}]'