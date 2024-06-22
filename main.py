import pygame as pg
import moderngl as mgl
import sys
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
class GraphicsEngine:
    def __init__(self, win_size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
        pg.init()
        self.WIN_SIZE = win_size
        # Set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # Create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags = pg.OPENGL | pg.DOUBLEBUF)
        # Force FPS mouse
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # Detect and use the created opengl context
        self.ctx = mgl.create_context(share=True)
        # by default, can be cw instead of ccw
        self.ctx.front_face= 'ccw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        #self.ctx.wireframe = True
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # Light
        self.light = Light()
        # Camera
        self.camera = Camera(self)
        # Scene
        self.mesh = Mesh(self)
        self.scene = Scene(self)
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
    
    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()
        pg.display.flip()
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()