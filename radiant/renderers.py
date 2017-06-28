import os

import numpy as np

from .materials import MeshBasicMaterial
from .scenes import Mesh


class Renderer:
    pass


def read_shaders(id):
    os.listdir(os.path.join(os.path.dirname(__file__), 'shaders'))


class ModernGLRenderer:
    def __init__(self, context):
        self.ctx = context
        self.model_stack = [np.eye(4, dtype='f4')]

    def render(self, scene, camera):
        def visit(node):
            self.model_stack.append(self.model_stack[-1] @ node.model)
            self.render_object(node, camera, self.model_stack[-1])
            for child in scene.children:
                visit(child)
            self.model_stack.pop()
        visit(scene)

    def render_object(self, object, camera, world):
        if isinstance(object, Mesh):
            if isinstance(object.material, MeshBasicMaterial):
                vert = ctx.vertex_shader(vertex_shader_source)
frag = ctx.fragment_shader(fragment_shader_source)
prog = ctx.program([vert, frag])
