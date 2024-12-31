import moderngl as mgl
import glm
from chunk_utils import *
class Chunk:
    def __init__(self, app, program, map_data, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        self.initialized = False
        self.program = program
        self.app = app
        self.ctx = app.ctx
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.map_data = map_data
        self.vertex_data, self.index_data = get_vertex_data(self.map_data)        
        self.camera = self.app.camera
    def re_init(self):
        self.vertex_data, self.index_data = get_vertex_data(self.map_data)  
        
    def on_init(self):
        if not self.initialized:
            self.initialized = True
            self.vbo = self.ctx.buffer(self.vertex_data, dynamic=True)        
            self.ibo = self.ctx.buffer(self.index_data, dynamic=True)   
            self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '1u 1u', *['in_vertinfo', 'in_color'])], self.ibo) # vbo_id, buffer format, attributes

            self.m_model = self.get_model_matrix()
            # mvp
            self.program['m_proj'].write(self.camera.m_proj)        
            self.program['m_view'].write(self.camera.m_view)
            self.program['m_model'].write(self.m_model)
        else:
            self.vbo.release()
            self.ibo.release()
            self.vbo = self.ctx.buffer(self.vertex_data, dynamic=True)        
            self.ibo = self.ctx.buffer(self.index_data, dynamic=True)   
            self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '1u 1u', *['in_vertinfo', 'in_color'])], self.ibo) # vbo_id, buffer format, attributes

    def destroy(self):
        self.vbo.release()
        self.ibo.release()
        self.program.destroy()
        self.vao.release()
    def update_pos(self, pos):
        self.pos = pos
        self.m_model = self.get_model_matrix()
    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        return m_model
    def render(self):
        self.update()
        self.vao.render()
    def update(self):
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        self.program['light_dir'].write(self.app.scene.environment.sun)
