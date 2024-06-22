import numpy as np
import moderngl as mgl
import glm
import random
CHUNK_SIZE = 16
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
        self.vertex_data, self.index_data = self.get_vertex_data()        
        self.camera = self.app.camera
    def re_init(self):
        self.vertex_data, self.index_data = self.get_vertex_data() 
        
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
    def is_blocked(self,x,y,z):
        if x < 0 or x > CHUNK_SIZE-1:
            return False
        if y < 0 or y > CHUNK_SIZE-1:
            return False
        if z < 0 or z > CHUNK_SIZE-1:
            return False
        if self.map_data[x][y][z] == 1:
            return True
        return False
   
    def add_face(self, v_list, norm_id, v_idx, c_list, color, *positions):
        for pos in positions:
            v_list[v_idx] = pos[0] << 27 | pos[1] << 22 | pos[2] << 17 | norm_id << 14
            c_list[v_idx] = color
            v_idx = v_idx + 1
        return v_idx
    def get_vertex_data(self):
        vertices = np.empty(CHUNK_SIZE * CHUNK_SIZE * CHUNK_SIZE * 24, dtype='uint32')
        v_idx = 0
        colors = np.empty(CHUNK_SIZE * CHUNK_SIZE * CHUNK_SIZE * 24, dtype='uint32')
        indices = []
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    color = random.randint(0, 0XFFFFFFFF)
                    if self.map_data[x][y][z] == 0:
                        continue
                    v0 = (0 + x, 0 + y, 1 + z)
                    v1 = (1 + x, 0 + y, 1 + z)
                    v2 = (1 + x, 1 + y, 1 + z)
                    v3 = (0 + x, 1 + y, 1 + z)

                    v4 = (0 + x, 0 + y, 0 + z)
                    v5 = (1 + x, 0 + y, 0 + z)
                    v6 = (1 + x, 1 + y, 0 + z)
                    v7 = (0 + x, 1 + y, 0 + z)
                    
                    if not self.is_blocked(x,y,z+1):
                        # Front face
                        indices.extend([0 + v_idx,1 + v_idx,2 + v_idx])
                        indices.extend([0 + v_idx,2 + v_idx,3 + v_idx])
                        
                        v_idx = self.add_face(vertices,0,v_idx,colors,color,v0,v1,v2,v3)
                    if not self.is_blocked(x,y,z-1):
                        # Back face
                        indices.extend([0 + v_idx,3 + v_idx,2 + v_idx])
                        indices.extend([0 + v_idx,2 + v_idx,1 + v_idx])

                        v_idx = self.add_face(vertices,1,v_idx,colors,color,v7,v4,v5,v6)
                    if not self.is_blocked(x-1,y,z):
                        # Left face
                        indices.extend([3 + v_idx,2 + v_idx,1 + v_idx])
                        indices.extend([1 + v_idx,0 + v_idx,3 + v_idx])
                        
                        v_idx = self.add_face(vertices,2,v_idx,colors,color,v0,v4,v7,v3)
                    if not self.is_blocked(x+1,y,z):
                        # Right face
                        indices.extend([3 + v_idx,1 + v_idx,0 + v_idx])
                        indices.extend([2 + v_idx,3 + v_idx,0 + v_idx])
                        
                        v_idx = self.add_face(vertices,3,v_idx,colors,color,v1,v2,v5,v6)
                    if not self.is_blocked(x,y+1,z):
                        # Top face
                        indices.extend([0 + v_idx,2 + v_idx,1 + v_idx])
                        indices.extend([0 + v_idx,3 + v_idx,2 + v_idx])
                        
                        v_idx = self.add_face(vertices,4,v_idx,colors,color,v2,v3,v7,v6)
                    if not self.is_blocked(x,y-1,z):
                        # Bottom face
                        indices.extend([1 + v_idx,0 + v_idx,2 + v_idx])
                        indices.extend([2 + v_idx,3 + v_idx,1 + v_idx])
                        
                        v_idx = self.add_face(vertices,5,v_idx,colors,color,v0,v1,v4,v5)
        #colors = np.array(colors, dtype="uint32")
        vertices = np.hstack( list(zip(vertices[:v_idx],colors)) )
        indices = np.array(indices, dtype='i4')
        return (vertices, indices)