import numpy as np
from surfaces.surface import Surface
from material import Material
from light import Light
from scene_settings import SceneSettings
from camera import Camera
from light_hit import LightHit
from rays.view_ray import ViewRay

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
                
        # 2. Initialise surfaces with materials, and camera point
        for s in self.surfaces:
            s.set_material(self.materials[s.material_index])
            s.set_p0(self.camera.position)

    def render(self):
        # pixel in np.array([(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)])
        image = np.zeros((*self.output_dimensions, 3), dtype=float)
        i = 0
        hc = 0
        bg = 0
        materials = set()
        print(f'bg_color={self.scene_settings.background_color}')
        woo = 0
        for pixel in self.image_pixels():
            i += 1
            # if np.all(pixel == np.array([250, 70])): # yellow
            #     pass
            if i % 25000 == 0:
                print(f'Epoch {i}...')
            # render pixel
            view_ray = self.camera.get_pixel_ray(pixel)
            hit = self.find_intersection(view_ray)
            if hit:
            # trace light - build objects tree/list
            # light_trace = self.build_light_trace(hit.surface)
                hc += 1
                materials.add(hit.surface.material)
                color = self.apply_light_trace(pixel, hit.surface)
            else:
                bg += 1
                color = self.scene_settings.background_color
            # print(f'Pixel {pixel}: color {color}')
            if color == self.scene_settings.background_color:
                woo += 1
            image[tuple(pixel)] = color

        image = np.array(image * 255, dtype=np.uint8)
        print(f'Image total: bg={bg}, hit color={hc}, woo={woo}')
        print(f'Hit materials: {materials} ')
        print(f'No of colors: {set([tuple(a) for a in image.reshape(-1, 3).tolist()])}, count={[(c,[tuple(a) for a in image.reshape(-1, 3).tolist()].count(c)) for c in set([tuple(a) for a in image.reshape(-1, 3).tolist()])]} ')

                
        return image

    def find_intersection(self, view_ray):
        best_hit = None
        for surface in self.surfaces:
            alpha = surface.calculate_intersection_factor(view_ray)
            if alpha < 0:
                continue
            hit = LightHit(surface, alpha)
            if not best_hit or hit < best_hit:
                best_hit = hit
                
        # if best_hit:
        # b;u    print(f'best hit alpha={hit.alpha}! surface %s' % (surface, ))

        return best_hit

    def image_pixels(self):
        pixels = list()
        # np.array([(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)])
        pixels = np.indices(self.output_dimensions)
        pixels = pixels.reshape(2, -1).T
        return pixels
    
    def build_light_trace(self, hitting_surface: Surface):
        trace = list()
        # TODO: trace the light ray and build the list, or tree
        return trace
    
    def apply_light_trace(self, pixel, surface: Surface):
        # print(f'light_color with {surface} material {surface.material}')
        return surface.material.diffuse_color