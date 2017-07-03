import os
from functools import lru_cache


@lru_cache()
def load_shader_sources():
    """
    Load all built-in shaders from filesystem.

    Returns
    -------
    dict of dict
        Mapping of shader key to mapping of shader type to shader source.
        Possible types are { 'vert', 'frag' }.
    """
    shader_sources = {}
    shader_path = os.path.join(os.path.dirname(__file__), 'shaders')
    for filename in os.listdir(shader_path):
        base, ext = os.path.splitext(filename)
        shader_sources[base] = {}
        with open(os.path.join(shader_path, filename)) as fh:
            shader_sources[base][ext[1:]] = fh.read()
    return shader_sources


class Material:
    def __init__(self, shaders=None):
        self.shaders = shaders or {}


class MeshBasicMaterial(Material):
    def __init__(self, color=(255, 255, 255)):
        super().__init__(load_shader_sources()['meshbasic'])
        self.color = color
