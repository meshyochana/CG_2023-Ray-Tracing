import numpy as np

from light_hit import LightHit
from material import Material
from scene_settings import SceneSettings
from surfaces.surface import Surface
from rays.ray import Ray

class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, radius):
        self.position = np.array(position)
        self.color = np.array(color)
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.radius = radius
        self.shadow_rays_num = 3 #int(SceneSettings.root_number_shadow_rays)

    def get_intensity(self, point: np.array, objects):
        #return 1
        ray_vector = normalize(point - self.position)

        # calculate the the plane constant d, according to: ax+by+cz+d=0
        d = -np.dot(self.position,ray_vector) 

        # find an arbitrary point in the plane
        idx = np.argmax(abs(ray_vector)) #to ensure we don't divide by 0
        plane_point = np.zeros(3)
        plane_point[idx] = -(d + ray_vector[(idx+1)%3] + ray_vector[(idx+2)%3])/ray_vector[idx]
        plane_point[(idx+1)%3] = 1 # arbitrary choise of parametrization
        plane_point[(idx+2)%3] = 1 # arbitrary choise of parametrization

        # find an orthonormal base to span the plane
        paralel_vec_1 = normalize(plane_point - self.position)
        paralel_vec_2 = normalize(np.cross(paralel_vec_1,ray_vector))

        bottom_left_rect = self.position-0.5*self.radius*(paralel_vec_1+paralel_vec_2)
        hit_percentage = self.hit_counter(point, bottom_left_rect, paralel_vec_1, paralel_vec_2, objects)

        return (1 - self.shadow_intensity) + (self.shadow_intensity * hit_percentage)       

    def hit_counter(self, point, bottom_left_rect, paralel_vec_1, paralel_vec_2, objects):
        hit_count = (self.shadow_rays_num)**2
        for i in range(self.shadow_rays_num):
            for j in range(self.shadow_rays_num):
                cell = bottom_left_rect +\
                ((i + np.random.uniform()) * paralel_vec_1 +\
                (j + np.random.uniform()) * paralel_vec_2 *\
                (self.radius/self.shadow_rays_num))

                #shadow_ray = normalize(point - cell)
                shadow_ray = Ray(point, point - cell)
                
                for obj in objects:
                    if obj.calculate_intersection_factor(shadow_ray)>0: # intersection is detected
                        hit_count -= 1

        hit_percentage = hit_count/float(self.shadow_rays_num)**2
        return hit_percentage
    


def normalize(v):
    v_normalized = v / np.linalg.norm(v)
    return v_normalized



