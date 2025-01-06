from pygame.locals import *
from OpenGL import GL
import numpy as np


def compile_shader(source, shader_type):
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        raise RuntimeError(GL.glGetShaderInfoLog(shader))
    return shader


def create_shader_program(vertex_source, fragment_source):
    vertex_shader = compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
    program = GL.glCreateProgram()
    GL.glAttachShader(program, vertex_shader)
    GL.glAttachShader(program, fragment_shader)
    GL.glLinkProgram(program)
    if not GL.glGetProgramiv(program, GL.GL_LINK_STATUS):
        raise RuntimeError(GL.glGetProgramInfoLog(program))
    GL.glDeleteShader(vertex_shader)
    GL.glDeleteShader(fragment_shader)
    return program


class BaseShader:
    def __init__(self, vertex_shader, fragment_shader, screen_size):
        print(f"Creating FBO{screen_size}")
        self.screen_size = screen_size
        self.program = self.create_shader_program(vertex_shader, fragment_shader)
        self.vertex_buffer = self.create_vertex_buffer()
        self.shaderScreenWidth = GL.glGetUniformLocation(self.program, "screenWidth")
        self.shaderScreenHeight = GL.glGetUniformLocation(self.program, "screenHeight")
        self.texture = self.create_texture(screen_size)
        self.frameBuffer = self.createFrameBuffer()

    def createFrameBuffer(self):
        fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, fbo)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            GL.GL_COLOR_ATTACHMENT0,
            GL.GL_TEXTURE_2D,
            self.texture,
            0,
        )
        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer is not complete")
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        return fbo

    def create_texture(self, screen_size):
        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            screen_size[0],
            screen_size[1],
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        return texture

    def compile_shader(self, source, shader_type):
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            raise RuntimeError(GL.glGetShaderInfoLog(shader))
        return shader

    def create_shader_program(self, vertex_source, fragment_source):
        program = GL.glCreateProgram()
        vertex_shader = self.compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        GL.glAttachShader(program, vertex_shader)
        GL.glAttachShader(program, fragment_shader)
        GL.glLinkProgram(program)
        if not GL.glGetProgramiv(program, GL.GL_LINK_STATUS):
            raise RuntimeError(GL.glGetProgramInfoLog(program))
        return program

    def create_vertex_buffer(self):
        vertices = np.array(
            [-1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0], dtype=np.float32
        )

        vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW
        )
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        return vertex_buffer

    def drawSetup(self):
        pass

    def draw(self):
        GL.glUseProgram(self.program)
        self.drawSetup()
        GL.glUniform1f(self.shaderScreenWidth, self.screen_size[0])
        GL.glUniform1f(self.shaderScreenHeight, self.screen_size[1])
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buffer)
        position_location = GL.glGetAttribLocation(self.program, "position")
        GL.glEnableVertexAttribArray(position_location)
        GL.glVertexAttribPointer(
            position_location, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None
        )

        GL.glDrawArrays(GL.GL_QUADS, 0, 4)

        GL.glDisableVertexAttribArray(position_location)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glUseProgram(0)
