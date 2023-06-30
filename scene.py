import numpy as np
from surfaces.surface import Surface
from material import Material
from light import Light
from scene_settings import SceneSettings
from camera import Camera
from light_hit import LightHit
from light_hit import CubeLightHit
from rays.light_ray import LightRay

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
            # s.set_p0(self.camera.position)

    def ray_trace(self, ray, excluded_surfaces=[]):
        hits = self.intersect(ray, excluded_surfaces)

        # Go backwards to find the transparency color, start from background color
        total_color = self.scene_settings.background_color
        if len(hits) > 1:
            pass
            # print('a')

        for hit in hits[::-1]:
            current_color = self.calc_diffuse_and_spec(hit)
            reflection_color = self.calc_reflection_color(hit)
            # if ray.ttl >= 1:
                # print(f'{type(hit)} with {type(hit.surface)}: diffspec={current_color} reflection={reflection_color}')
            total_color = current_color * (1 - hit.surface.material.transparency) + total_color * hit.surface.material.transparency + reflection_color

        return total_color

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
            if np.all(pixel == np.array([270, 150])): # yellow
                pass
            if i % 25000 == 0:
                print(f'Epoch {i}...')
            # render pixel
            view_ray = self.camera.get_pixel_ray(pixel)
            color = self.ray_trace(view_ray)
            image[tuple(pixel)] = color

        image_clipped = np.clip(image, 0, 1)
        image_result = np.array(image_clipped * 255, dtype=np.uint8)
        print(f'Image total: bg={bg}, hit color={hc}, woo={woo}')
        print(f'Hit materials: {materials} ')
        # print(f'No of colors: {set([tuple(a) for a in image.reshape(-1, 3).tolist()])}, count={[(c,[tuple(a) for a in image.reshape(-1, 3).tolist()].count(c)) for c in set([tuple(a) for a in image.reshape(-1, 3).tolist()])]} ')
                
        return image_result

    """
    def find_intersection(self, view_ray):
        best_hit = None
        for surface in self.surfaces:
            alpha = surface.calculate_intersection_factor(view_ray)
            if alpha < 0:
                continue
            hit = LightHit(surface, view_ray, alpha)
            if not best_hit or hit < best_hit:
                best_hit = hit
                
        # if best_hit:
        # b;u    print(f'best hit alpha={hit.alpha}! surface %s' % (surface, ))

        return best_hit
    """
    def crop_hits_until_non_transparent(self, hits):
        hits_until_stop = hits
        for i in range(len(hits)):
            if 0 == hits[i].surface.material.transparency:
                hits_until_stop = hits[: i + 1]
                break
                
        return hits_until_stop
    
    def intersect(self, ray, excluded_surfaces=[]):
        all_hits = [s.intersect(ray) for s in self.surfaces if s not in excluded_surfaces]
        ordered_hits = sorted([h for h in all_hits if h is not None])
        hits_until_stop = self.crop_hits_until_non_transparent(ordered_hits)

        return hits_until_stop

    def image_pixels(self):
        pixels = list()
        # np.array([(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)])
        pixels = np.indices(self.output_dimensions)#[:20:260,127:140]
        # pixels = np.array([(246,127)])
        pixels = pixels.reshape(2, -1).T
        return pixels
    
    def build_light_trace(self, hitting_surface: Surface):
        trace = list()
        # TODO: trace the light ray and build the list, or tree
        return trace
    
    def calc_reflection_color(self, hit: LightHit):
        if 1 >= hit.ray.ttl:
            return np.zeros((3, ), dtype=float)
        
        ray = hit.get_reflection_ray()
        ray_color = self.ray_trace(ray, [hit.surface])
        # print(ray_color)
        color = np.multiply(hit.surface.material.reflection_color, ray_color)
        if not np.all(color == np.array([0,0,0])):
            pass
        return color
    
    def calc_diffuse_and_spec(self, hit: LightHit):
        # print(f'light_color with {surface} material {surface.material}')
        diffuse_color = hit.surface.material.diffuse_color
        I_diffusion = 0
        I_specular = 0
        for light in self.lights:
            light_ray = LightRay(light, hit.position)
            I = light.get_intensity(self, hit)
            I_diffusion += self.get_diffuse_color(I, hit, light)
            I_specular += self.get_specular_color(I, hit, light_ray, light)

        diffuse_color = np.multiply(hit.surface.material.diffuse_color, I_diffusion)
        specular_color = np.multiply(hit.surface.material.specular_color, I_specular)
        
        color = diffuse_color + specular_color
        
        return color
    
    def get_diffuse_color(self, light_intensity, hit: LightHit, light: Light) -> np.array:
        L = normalize(light.position - hit.position)
        N = hit.get_normal()
        n_dot_l = np.dot(N, L)
        if n_dot_l < 0:
            diffuse_color = np.zeros((3, ), dtype=float)
        else:
            # print(f'diffuse ndotl={n_dot_l}! zeroing')
            diffuse_color = light_intensity * n_dot_l * light.color

        return diffuse_color
    
    def get_specular_color(self, light_intensity, hit: LightHit, light_ray: LightRay, light: Light) -> np.array:
        V = -hit.ray.vto
        R = hit.surface.get_reflection_ray(light_ray, hit).vto
        V_dot_R = np.dot(V, R)
        if V_dot_R < 0:
            # print(f'ndotl={n_dot_l}! zeroing')
            specular_color = np.zeros((3, ), dtype=float)
        else:
            n_dot_l_pow = np.power(V_dot_R, hit.surface.material.shininess)
            specular_color = light.color * light_intensity * n_dot_l_pow * light.specular_intensity

        return specular_color
    

def normalize(v):
    v_normalized = v / np.linalg.norm(v)
    return v_normalized