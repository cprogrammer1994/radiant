from collections import OrderedDict
from functools import lru_cache

import ModernGL

import numpy as np

from .base import Renderer
from ..scenes import Mesh


class ModernGLRenderer(Renderer):
    def __init__(self, context):
        self.ctx = context
        self.model_stack = [np.eye(4, dtype='f4')]

    def render(self, scene, camera):
        """
        Render scene from the camera viewpoint.
        """
        view_projection = camera.view * camera.projection

        def visit(node):
            self.model_stack.append(self.model_stack[-1] * node.model)
            self.render_object(node, view_projection, self.model_stack[-1])
            for child in node.children:
                visit(child)
            self.model_stack.pop()

        # get going
        self.ctx.enable(ModernGL.DEPTH_TEST)
        self.ctx.clear(0.9, 0.9, 0.9)
        visit(scene)

    @lru_cache(maxsize=None)
    def get_program(self, material):
        mapping = OrderedDict([
            ('vert', self.ctx.vertex_shader),
            ('frag', self.ctx.fragment_shader),
        ])
        shaders = [mapping[key](source) for key, source in material.shaders.items()]
        return self.ctx.program(shaders)

    def render_object(self, node, view_projection, world):
        if isinstance(node, Mesh):
            prog = self.get_program(node.material)
