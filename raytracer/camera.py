import numpy as np

class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = np.array(position)
        self.look_at = np.array(look_at)
        self.up_vector = np.array(up_vector)
        self.screen_distance = screen_distance
        self.screen_width = screen_width
        self.Rx = None
        self.Ry = None
        self.ratio = None
        self._init_directions()

    def _init_directions(self):
        vto = self.look_at / np.linalg.norm(self.look_at)
        vup = self.up_vector / np.linalg.norm(self.up_vector)
        vright = np.cross(vto, vup)
        vright /= np.linalg.norm(vright)
        vup_tilde = np.cross(vright, vto)
        vup_tilde /= np.linalg.norm(vup_tilde)
        self.vto = vto
        self.vright = vright
        self.vup_tilde = vup_tilde
        self.center = self.position + self.screen_distance * vto

    def init_resolution(self, Rx, Ry):
        ratio = self.screen_width / Rx
        self.Rx = Rx
        self.Ry = Ry
        self.ratio = ratio

    def get_pixel_coordinate(self, pixel):
        i, j = pixel
        vright_factor = (j - np.floor(self.Rx / 2)) * self.ratio
        vup_factor = (i - np.floor(self.Ry / 2)) * self.ratio
        view_ray = vright_factor * self.vright - vup_factor + self.vup_tilde
        Pc = self.center + view_ray
        return Pc