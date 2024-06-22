import numpy as np
import moderngl as mgl
import glm
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
    def pack_data(self, x, y, z, norm_id):
        return x << 27 | y << 22 | z << 17 | norm_id << 14
    def on_init(self):
        self.initialized = True
        self.vbo = self.ctx.buffer(self.vertex_data)        
        self.ibo = self.ctx.buffer(self.index_data)   
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '1u', *['in_vertinfo'])], self.ibo) # vbo_id, buffer format, attributes
        #self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f 3f', *['in_normal', 'in_position'])], self.ibo) # vbo_id, buffer format, attributes

        self.m_model = self.get_model_matrix()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)        
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # lights
        self.program['light.position'].write(self.app.light.position)        
        self.program['light.Ia'].write(self.app.light.Ia)        
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
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
        #m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        #m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        #m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))
        #m_model = glm.scale(m_model, self.scale)
        return m_model
    def render(self):
        self.update()
        self.vao.render()
    def update(self):
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
    
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
    def get_vertex_data(self):
        vertices = []
        indices = []
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    if self.map_data[x][y][z] == 0:
                        continue
                    if not self.is_blocked(x,y,z+1):
                        # Front face
                        indices.append(tuple(map(lambda i: i + len(vertices),[0,1,2])))
                        indices.append(tuple(map(lambda i: i + len(vertices),[0,2,3])))
                        
                        vertices.append(self.pack_data(0 + x, 0 + y, 1 + z,0))
                        vertices.append(self.pack_data(1 + x, 0 + y, 1 + z,0))
                        vertices.append(self.pack_data(1 + x, 1 + y, 1 + z,0))
                        vertices.append(self.pack_data(0 + x, 1 + y, 1 + z,0))
                        # normals.append(( 0, 0, 1))
                        # normals.append(( 0, 0, 1))
                        # normals.append(( 0, 0, 1))
                        # normals.append(( 0, 0, 1))
                    if not self.is_blocked(x,y,z-1):
                        # Back face
                        indices.append(tuple(map(lambda i: i + len(vertices),[0,3,2])))
                        indices.append(tuple(map(lambda i: i + len(vertices),[0,2,1])))

                        vertices.append(self.pack_data(0 + x, 1 + y, 0 + z,1))
                        vertices.append(self.pack_data(0 + x, 0 + y, 0 + z,1))
                        vertices.append(self.pack_data(1 + x, 0 + y, 0 + z,1))
                        vertices.append(self.pack_data(1 + x, 1 + y, 0 + z,1))

                        # normals.append(( 0, 0,-1))
                        # normals.append(( 0, 0,-1))
                        # normals.append(( 0, 0,-1))
                        # normals.append(( 0, 0,-1))
                    if not self.is_blocked(x-1,y,z):
                        # Left face
                        indices.append(tuple(map(lambda i: i + len(vertices),[3,2,1])))
                        indices.append(tuple(map(lambda i: i + len(vertices),[1,0,3])))
                        
                        vertices.append(self.pack_data(0 + x, 0 + y, 1 + z,2))
                        vertices.append(self.pack_data(0 + x, 0 + y, 0 + z,2))
                        vertices.append(self.pack_data(0 + x, 1 + y, 0 + z,2))
                        vertices.append(self.pack_data(0 + x, 1 + y, 1 + z,2))

                        # normals.append((-1, 0, 0))
                        # normals.append((-1, 0, 0))
                        # normals.append((-1, 0, 0))
                        # normals.append((-1, 0, 0))
                    if not self.is_blocked(x+1,y,z):
                        # Right face
                        indices.append(tuple(map(lambda i: i + len(vertices),[3,1,0])))
                        indices.append(tuple(map(lambda i: i + len(vertices),[2,3,0])))
                        
                        vertices.append(self.pack_data(1 + x, 0 + y, 1 + z,3))
                        vertices.append(self.pack_data(1 + x, 1 + y, 1 + z,3))
                        vertices.append(self.pack_data(1 + x, 0 + y, 0 + z,3))
                        vertices.append(self.pack_data(1 + x, 1 + y, 0 + z,3))

                  
                        # normals.append(( 1, 0, 0))
                        # normals.append(( 1, 0, 0))
                        # normals.append(( 1, 0, 0))
                        # normals.append(( 1, 0, 0))
                    if not self.is_blocked(x,y+1,z):
                        # Top face
                        indices.append(tuple(map(lambda i: i + len(vertices),[0,2,1])))
                        indices.append(tuple(map(lambda i: i + len(vertices),[0,3,2])))
                        
                        vertices.append(self.pack_data(1 + x, 1 + y, 1 + z,4))
                        vertices.append(self.pack_data(0 + x, 1 + y, 1 + z,4))
                        vertices.append(self.pack_data(0 + x, 1 + y, 0 + z,4))
                        vertices.append(self.pack_data(1 + x, 1 + y, 0 + z,4))

                       
                        # normals.append(( 0, 1, 0))
                        # normals.append(( 0, 1, 0))
                        # normals.append(( 0, 1, 0))
                        # normals.append(( 0, 1, 0))
                    if not self.is_blocked(x,y-1,z):
                        # Bottom face
                        indices.append(tuple(map(lambda i: i + len(vertices),[1,0,2])))
                        indices.append(tuple(map(lambda i: i + len(vertices),[2,3,1])))
                        
                        vertices.append(self.pack_data(0 + x, 0 + y, 1 + z,5))
                        vertices.append(self.pack_data(1 + x, 0 + y, 1 + z,5))
                        vertices.append(self.pack_data(0 + x, 0 + y, 0 + z,5))
                        vertices.append(self.pack_data(1 + x, 0 + y, 0 + z,5))

                     
                        # normals.append(( 0, -1, 0))
                        # normals.append(( 0, -1, 0))
                        # normals.append(( 0, -1, 0))
                        # normals.append(( 0, -1, 0))
        vertices = np.array(vertices, dtype="uint32")
        indices = np.array(indices, dtype='i4').flatten()
        return (vertices, indices)