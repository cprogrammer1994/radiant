import radiant
import ModernGL


def test_render():
    ctx = ModernGL.create_standalone_context()

    renderer = radiant.ModernGLRenderer(ctx)

    scene = radiant.Scene()

    cube_geom = radiant.CubeGeometry()
    red = radiant.MeshBasicMaterial(color=(255, 0, 0))
    cube = radiant.Mesh(cube_geom, red)

    scene.children.append(cube)

    camera = radiant.PerspectiveCamera([10, 10, 10], [0, 0, 0], up=[0, 1, 0])

    renderer.render(scene, camera)
