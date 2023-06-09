import numpy as np
from surfaces.surface import Surface
from material import Material
from light import Light
from scene_settings import SceneSettings

class Scene():
    def __init__(self, camera, scene_settings: SceneSettings, objects, width: int, height: int):
        self.camera = camera
        self.scene_settings = scene_settings
        self._set_objects(objects)
        self.output_dimensions = (width, height, )

    def _set_objects(self, objects):
        # ...
        self.materials = list()
        self.surfaces = list()
        self.lights = list()
        #  Divide into lists
        for o in objects:
            if isinstance(o, Surface):
                o.set_material(self.materials)
                self.surfaces.append(o)
            elif isinstance(o, Light):
                self.lights.append(o)
            elif isinstance(o, Material):
                self.materials.append(o)
            else:
                raise TypeError('Unknown object type - neither Surface, Light or Material')
                
        # 2. Initialise surfaces with materials
        for s in self.surfaces:
            s.set_material(self.materials[s.material_index])

    def render(self):
        # TODO:
        for pixel in self.image_pixels():
            # render pixel
            transformed_pixel = self.transform_pixel(pixel)
            # trace light - build objects tree/list
            light_trace = self.build_light_trace(transformed_pixel)
            color = self.apply_light_trace(pixel, light_trace)
        pass

    def image_pixels(self):
        pixels = list()
        # np.array([(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)])
        pixels = np.indices(self.output_dimensions)
        pixels = pixels.reshape(2, -1).T
        return pixels
    
    def transform_pixel(self, pixel):
        # TODO: transform the pixel from the final image to absolute coordinates
        return pixel
    
    def build_light_trace(self, tpixel):
        trace = list()
        # TODO: trace the light ray and build the list, or tree
        return trace
    
    def apply_light_trace(pixel, light_trace: list):
        color = 0
        for object in light_trace:
            # color += object.???
            pass
        
        return color