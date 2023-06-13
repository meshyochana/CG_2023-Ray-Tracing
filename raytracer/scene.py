import numpy as np
from surfaces.surface import Surface
from material import Material
from light import Light
from scene_settings import SceneSettings
from camera import Camera
from light_hit import LightHit

class Scene():
    def __init__(self, camera: Camera, scene_settings: SceneSettings, objects: list, width: int, height: int):
        self.camera = camera
        self.scene_settings = scene_settings
        self._set_objects(objects)
        self.output_dimensions = (width, height, )
        self.camera.init_resolution(*self.output_dimensions)

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
            s.set_p0(self.camera.center)

    def render(self):
        # pixel in np.array([(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)])
        image = np.zeros((*self.output_dimensions, 3))
        i = 0
        for pixel in self.image_pixels():
            i += 1
            if i % 25000 == 0:
                print(f'Epoch {i}...')
            # render pixel
            view_ray = self.construct_ray_through_pixel(pixel)
            hit = self.find_intersection(view_ray)
            if hit:
            # trace light - build objects tree/list
            # light_trace = self.build_light_trace(hit.surface)
                color = self.apply_light_trace(pixel, hit.surface)
            else:
                color = self.scene_settings.background_color
            image[pixel] = color
        
        return image

    def find_intersection(self, view_ray):
        best_hit = None
        for surface in self.surfaces:
            alpha = surface.calculate_intersection_factor(view_ray)
            hit = LightHit(surface, alpha)
            if not hit:
                continue
            if not best_hit or hit < best_hit:
                best_hit = hit

        return best_hit

    def image_pixels(self):
        pixels = list()
        # np.array([(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)])
        pixels = np.indices(self.output_dimensions)
        pixels = pixels.reshape(2, -1).T
        return pixels
    
    def construct_ray_through_pixel(self, pixel):
        camera_pixel = self.camera.get_pixel_coordinate(pixel)
        view_ray = camera_pixel - self.camera.center
        return view_ray 
    
    def build_light_trace(self, hitting_surface: Surface):
        trace = list()
        # TODO: trace the light ray and build the list, or tree
        return trace
    
    def apply_light_trace(self, pixel, surface: Surface):
        return surface.material.diffuse_color