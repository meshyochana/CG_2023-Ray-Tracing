from surfaces.surface import Surface

class LightHit:
    def __init__(self, surface: Surface, alpha: float):
        self.surface = surface
        self.alpha = alpha

    def __lt__(self, other):
        return self.alpha < other.alpha