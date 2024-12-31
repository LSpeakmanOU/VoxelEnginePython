from numba import jit
import numpy as np
import random
CHUNK_SIZE = 16
@jit(nopython=True)
def is_blocked(x,y,z, map_data):
    if x < 0 or x > CHUNK_SIZE-1:
        return False
    if y < 0 or y > CHUNK_SIZE-1:
        return False
    if z < 0 or z > CHUNK_SIZE-1:
        return False
    if map_data[x][y][z] == 1:
        return True
    return False
@jit(nopython=True)
def add_face(v_list, norm_id, v_idx, c_list, color, *positions):
    for pos in positions:
        v_list[v_idx] = pos[0] << 27 | pos[1] << 22 | pos[2] << 17 | norm_id << 14
        c_list[v_idx] = color
        v_idx = v_idx + 1
    return v_idx
@jit(nopython=True)
def get_vertex_data(map_data):
    vertices = np.empty(CHUNK_SIZE * CHUNK_SIZE * CHUNK_SIZE * 24, dtype='uint32')
    v_idx = 0
    colors = np.empty(CHUNK_SIZE * CHUNK_SIZE * CHUNK_SIZE * 24, dtype='uint32')
    indices = []
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                color = random.randint(0, 0XFFFFFFFF)
                if map_data[x][y][z] == 0:
                    continue
                v0 = (0 + x, 0 + y, 1 + z)
                v1 = (1 + x, 0 + y, 1 + z)
                v2 = (1 + x, 1 + y, 1 + z)
                v3 = (0 + x, 1 + y, 1 + z)

                v4 = (0 + x, 0 + y, 0 + z)
                v5 = (1 + x, 0 + y, 0 + z)
                v6 = (1 + x, 1 + y, 0 + z)
                v7 = (0 + x, 1 + y, 0 + z)
                
                if not is_blocked(x,y,z+1,map_data):
                    # Front face
                    indices.extend([0 + v_idx,1 + v_idx,2 + v_idx])
                    indices.extend([0 + v_idx,2 + v_idx,3 + v_idx])
                    
                    v_idx = add_face(vertices,0,v_idx,colors,color,v0,v1,v2,v3)
                if not is_blocked(x,y,z-1,map_data):
                    # Back face
                    indices.extend([0 + v_idx,3 + v_idx,2 + v_idx])
                    indices.extend([0 + v_idx,2 + v_idx,1 + v_idx])

                    v_idx = add_face(vertices,1,v_idx,colors,color,v7,v4,v5,v6)
                if not is_blocked(x-1,y,z,map_data):
                    # Left face
                    indices.extend([3 + v_idx,2 + v_idx,1 + v_idx])
                    indices.extend([1 + v_idx,0 + v_idx,3 + v_idx])
                    
                    v_idx = add_face(vertices,2,v_idx,colors,color,v0,v4,v7,v3)
                if not is_blocked(x+1,y,z,map_data):
                    # Right face
                    indices.extend([3 + v_idx,1 + v_idx,0 + v_idx])
                    indices.extend([2 + v_idx,3 + v_idx,0 + v_idx])
                    
                    v_idx = add_face(vertices,3,v_idx,colors,color,v1,v2,v5,v6)
                if not is_blocked(x,y+1,z,map_data):
                    # Top face
                    indices.extend([0 + v_idx,2 + v_idx,1 + v_idx])
                    indices.extend([0 + v_idx,3 + v_idx,2 + v_idx])
                    
                    v_idx = add_face(vertices,4,v_idx,colors,color,v2,v3,v7,v6)
                if not is_blocked(x,y-1,z,map_data):
                    # Bottom face
                    indices.extend([1 + v_idx,0 + v_idx,2 + v_idx])
                    indices.extend([2 + v_idx,3 + v_idx,1 + v_idx])
                    
                    v_idx = add_face(vertices,5,v_idx,colors,color,v0,v1,v4,v5)
    #colors = np.array(colors, dtype="uint32")
    vertices = np.column_stack((vertices[:v_idx],colors[:v_idx]))
    indices = np.array(indices, dtype='i4')
    return (vertices, indices)