from model import *
from environment import Environment
class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.environment = Environment(app)
        self.load()
    def add_object(self, obj):
        self.objects.append(obj)
    
    def load(self):
        app = self.app
        add = self.add_object
        add(Quad(app))
    def render(self):
        self.environment.render()
        for obj in self.objects:
            obj.render()