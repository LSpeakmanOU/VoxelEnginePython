import numpy as np

class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos[0] = basicVBO(ctx)
    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]
class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo, self.ibo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None

    def get_vbo(self):
        vertex_data, index_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)        
        ibo = self.ctx.buffer(index_data)
        return (vbo, ibo)
    def destroy(self):
        self.vbo.release()
class basicVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f 3f'
        self.attribs = ['in_normal', 'in_position']
    
    def get_vertex_data(self):
        vertex_data = [
            (1.0, 1.0, 0.0),
            (-1.0, 1.0, 0.0),
            (1.0, -1.0, 0.0),
            (-1.0, -1.0, 0.0)
        ]
        
        indices = [(0,1,2),(2,1,3)]
        
        vertex_data = np.array(vertex_data, dtype="f4")
        normals = [(0,0,1),(0,0,1),(0,0,1),(0,0,1)]

        normals = np.array(normals, dtype='f4')

        vertex_data = np.hstack([normals, vertex_data])
        indices = np.array(indices, dtype='i4').flatten()
        return (vertex_data, indices)

# use ccw for triangle def
'''
normals_list = [( 0, 0, 1),     # forward
                        ( 1, 0, 0),     # right
                        ( 0, 0,-1),     # back
                        (-1, 0, 0),     # left
                        ( 0, 1, 0),     # top
                        ( 0,-1, 0),]    # bottom
        
vertices_list = [(-1, -1, 1),   # left bottom front
                         (1, -1, 1),    # right bottom front
                         (1, 1, 1),     # right top front
                         (-1, 1, 1),    # left top front
                         (-1, 1, -1),   # left top back
                         (-1, -1, -1),  # left bottom back
                         (1, -1, -1),   # right bottom back
                         (1, 1, -1)]    # right top back
'''