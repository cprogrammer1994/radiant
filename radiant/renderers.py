import os

import numpy as np

from .scenes import Mesh


class Renderer:
    pass


def get_shaders():
    shader_sources = {}
    shader_path = os.path.join(os.path.dirname(__file__), 'shaders')
    for filename in os.listdir(shader_path):
        base, ext = os.path.splitext(filename)
        shader_sources[base] = {}
        with open(os.path.join(shader_path, filename)) as fh:
            shader_sources[base][ext[1:]] = fh.read()
    return shader_sources


# eagerly read all the shader files
shader_sources = get_shaders()


class ModernGLRenderer:
    def __init__(self, context):
        self.ctx = context
        self.model_stack = [np.eye(4, dtype='f4')]
        self.program_cache = {}

    def render(self, scene, camera):
        view_projection = camera.view * camera.projection

        def visit(node):
            self.model_stack.append(self.model_stack[-1] * node.model)
            self.render_object(node, view_projection, self.model_stack[-1])
            for child in node.children:
                visit(child)
            self.model_stack.pop()
        visit(scene)

    def render_object(self, object, view_projection, world):
        if isinstance(object, Mesh):
            # first get the shader program
            prog = self.program_cache.get(object.material.id)
            if prog is None:
                # compile it if it does not exist yet
                shaders = []
                if 'vert' in shader_sources[object.material.id]:
                    shaders.append(self.ctx.vertex_shader(shader_sources[object.material.id]['vert']))
                if 'frag' in shader_sources[object.material.id]:
                    shaders.append(self.ctx.fragment_shader(shader_sources[object.material.id]['frag']))
                prog = self.ctx.program(shaders)
                self.program_cache[object.material.id] = prog

