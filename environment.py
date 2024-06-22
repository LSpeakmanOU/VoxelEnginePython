from chunk_mesh import Chunk, CHUNK_SIZE
from shader_program import ShaderProgram
import pygame as pg
import numpy as np
import glm
import opensimplex
import threading
import queue
import math
CHUNK_RENDER_DIST = 5
NOISE_RES = 0.9
class Environment:
    def __init__(self, app):
        self.app=app
        opensimplex.seed(1234)
        self.chunks = []
        self.chunk_map = {}
        self.program = ShaderProgram(app.ctx).programs["chunk"]
        self.to_generate = queue.Queue()
        threading.Thread(target=self.load_chunks, daemon=True).start()
        self.to_finish = queue.Queue()
        self.sun = glm.vec3(0.0,0.0,0.0)
        self.time = 0.0
    def build_chunk(self, loc):
        map_data =np.zeros((CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE), dtype='i1')
        for x_loc in range(CHUNK_SIZE):
            for z_loc in range(CHUNK_SIZE):
                noise = ((opensimplex.noise2(x=((x_loc / CHUNK_SIZE)+loc[0]) * NOISE_RES, y=((z_loc / CHUNK_SIZE)+loc[2]) * NOISE_RES) + 1) / 2)
                height = int(max(noise * CHUNK_SIZE, 1))
                for y in range(height):
                    map_data[x_loc][y][z_loc] = 1
        return map_data
    def add_chunk(self, loc):
        self.chunks.append(Chunk(self.app, self.program, self.build_chunk(loc), pos=(loc[0] * CHUNK_SIZE, loc[1] * CHUNK_SIZE, loc[2] * CHUNK_SIZE)))
        self.chunk_map[loc] = self.chunks[len(self.chunks)-1]
    def update(self):
        self.time += 0.01
        self.sun = glm.vec3(0.5,math.cos(self.time),0.0)
    def change_terrain(self, event):
        ray_data = self.get_ray_to_block()
        if not ray_data == None:
            last_block, chunk_pos, block_pos = ray_data
            if event.button == 1:
                if self.chunk_map[chunk_pos].map_data[block_pos[0]][block_pos[1]][block_pos[2]] == 1:
                    self.chunk_map[chunk_pos].map_data[block_pos[0]][block_pos[1]][block_pos[2]] = 0
                    self.to_generate.put(chunk_pos)
            if event.button == 3:
                if not last_block == None:
                    chunk_pos, block_pos = last_block
                    if self.chunk_map[chunk_pos].map_data[block_pos[0]][block_pos[1]][block_pos[2]] == 0:
                        self.chunk_map[chunk_pos].map_data[block_pos[0]][block_pos[1]][block_pos[2]] = 1
                        self.to_generate.put(chunk_pos)
    def render(self):
        self.update()
        if not self.to_finish.empty():
            new_chunk = self.to_finish.get()
            self.chunk_map[new_chunk].on_init()
            
        cam_chunk_coords = (int(self.app.camera.position.x / CHUNK_SIZE), int(self.app.camera.position.z / CHUNK_SIZE))
        for x in range(cam_chunk_coords[0]-CHUNK_RENDER_DIST, cam_chunk_coords[0]+CHUNK_RENDER_DIST):
            for z in range(cam_chunk_coords[1]-CHUNK_RENDER_DIST, cam_chunk_coords[1]+CHUNK_RENDER_DIST):
                curr_chunk = (x, 0, z)
                if curr_chunk in self.chunk_map:
                    if self.chunk_map[curr_chunk] == None or not self.chunk_map[curr_chunk].initialized:
                        continue
                    self.chunk_map[curr_chunk].render()
                else:
                    self.chunk_map[curr_chunk] = None
                    self.to_generate.put(curr_chunk)
    def load_chunks(self):
            while True:
                if not self.to_generate.empty():
                    new_chunk = self.to_generate.get()
                    if self.chunk_map[new_chunk] == None:
                        self.add_chunk(new_chunk)
                    else:
                        self.chunk_map[new_chunk].re_init()
                    self.to_finish.put(new_chunk)
    def get_ray_to_block(self):
        steps = 0
        pos = self.app.camera.position+glm.vec3(0,-1,0)
        last_block = None
        while steps < 20:
            if pos.y <= CHUNK_SIZE and pos.y >= 0:
                chunk_pos = (int((pos.x-(CHUNK_SIZE if pos.x<0 else 0)) / CHUNK_SIZE),0, int((pos.z-(CHUNK_SIZE if pos.z<0 else 0)) / CHUNK_SIZE))
                if chunk_pos in self.chunk_map and not self.chunk_map[chunk_pos] == None:
                    block_pos = (int(pos.x) % CHUNK_SIZE, int(pos.y) % CHUNK_SIZE, int(pos.z) % CHUNK_SIZE)
                    if self.chunk_map[chunk_pos].map_data[block_pos[0]][block_pos[1]][block_pos[2]] != 0:
                        return (last_block,chunk_pos, block_pos)
                    last_block = (chunk_pos, block_pos)
            pos += self.app.camera.mouse_ray
            steps+=1
        return None
