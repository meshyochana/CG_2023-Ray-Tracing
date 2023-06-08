class Scene():
    def __init__(self, camera, scene_settings, objects):
        self.camera = camera
        self.scene_settings = scene_settings
        self._set_objects(objects)

    def _set_objects(self, objects):
        # ...
        self.materials = list()
        self.objects = list()
        self.lights = list()

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
        # [(0,0), (0,1), ..., (0, 500), ..., (500, 0), ..., (500, 500)]
        # type: list or generator
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