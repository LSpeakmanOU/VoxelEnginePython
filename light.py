import glm

class Light:
    def __init__(self, position=(3,3,3), color=(1,1,1)):
        self.position = glm.vec3(position)
        self.dir = glm.vec3(-0.5,-0.5,0)
        self.color = glm.vec3(color)
        self.Ia = 0.05 * self.color # ambient
        self.Id = 0.8 * self.color # diffuse
        self.Is = 2.0 * self.color # specular

        