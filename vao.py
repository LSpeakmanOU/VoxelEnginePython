from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, ctx):
        self.ctx=ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        self.vaos[0] = self.get_vao(
            program=self.program.programs["model"],
            vbo=self.vbo.vbos[0])
    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], vbo.ibo) # vbo_id, buffer format, attributes
        return vao
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
        [vao.release() for vao in self.vaos.values()]