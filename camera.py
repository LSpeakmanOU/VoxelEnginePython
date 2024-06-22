import glm
import pygame as pg
FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05
class Camera:
    def __init__(self, app, position=(0, 10, 4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0,1,0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch=pitch
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)
        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0,1,0)))        
        self.up = glm.normalize(glm.cross(self.right, self.forward))
        self.mouse_ray = glm.vec3()
    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()        
        self.mouse_ray = self.get_mouse_ray()
    def get_mouse_ray(self):
        m_x = self.app.WIN_SIZE[0] / 2
        m_y = self.app.WIN_SIZE[1] / 2
        norm_x = (m_x * 2.0) / self.app.WIN_SIZE[0] - 1.0
        #norm_y = (m_y * 2.0) / self.app.WIN_SIZE[1] - 1.0
        norm_y = 1.0 - (m_y * 2.0) / self.app.WIN_SIZE[1]
        ray_nds = glm.vec3(norm_x, norm_y, 1.0)
        ray_clip = glm.vec4(ray_nds.xy, -1.0, 1.0)
        ray_eye = glm.inverse(self.m_proj) * ray_clip 
        ray_eye = glm.vec4(ray_eye.xy, -1.0, 0.0)
        ray_world = glm.normalize((glm.inverse(self.m_view) * ray_eye).xyz)
        return ray_world
    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity
    def get_view_matrix(self):
        # Looks at the origin, WRONG
        #return glm.lookAt(self.position, glm.vec3(0), self.up)
        return glm.lookAt(self.position, self.position + self.forward, self.up)
    
    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)