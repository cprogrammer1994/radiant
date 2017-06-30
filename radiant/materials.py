class Material:
    id = None


class MeshBasicMaterial(Material):
    id = 'meshbasic'

    def __init__(self, color=(255, 255, 255)):
        self.color = color
