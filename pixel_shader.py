from OpenGL import GL

vertex_shader_source = """
#version 330 core
layout(location = 0) in vec2 position;
void main() {
gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragment_shader_source = """
#version 330 core
out vec4 FragColor;
void main() {
vec2 uv = gl_FragCoord.xy / vec2(100.0, 800.0);
vec2 pixelated_uv = floor(uv * 10.0) / 10.0;
FragColor = vec4(uv, 0.0, 1.0);
}
"""


# Compile shader
def compile_shader(source, shader_type):
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        raise RuntimeError(GL.glGetShaderInfoLog(shader))
    return shader


# Create shader program
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


def createPixelShader():
    return create_shader_program(vertex_shader_source, fragment_shader_source)


import pygame
from pygame.locals import *
from OpenGL import GL
import math
import numpy as np

vertex_shader = """
#version 330
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330
uniform sampler2D screenTexture;
uniform float pixelSize;
uniform float screenHeight;
uniform float screenWidth;
out vec4 FragColor;
void main() {
    vec2 uv = gl_FragCoord.xy / vec2(screenWidth, screenHeight);
    vec2 pixelatedUV = floor(uv / pixelSize) * pixelSize;
    FragColor = texture(screenTexture, pixelatedUV);
}
"""


class MovingCircle:
    def __init__(self, radius, speed):
        self.radius = radius
        self.speed = speed
        self.angle = 0

    def draw(self):
        GL.glBegin(GL.GL_POLYGON)
        for i in range(360):
            theta = 2.0 * math.pi * i / 360
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            GL.glVertex2f(x, y)
        GL.glEnd()

    def update(self):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360


class PixelateShader:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.program = self.create_shader_program(vertex_shader, fragment_shader)
        self.pixel_size_location = GL.glGetUniformLocation(self.program, "pixelSize")
        self.shaderScreenWidth = GL.glGetUniformLocation(self.program, "screenWidth")
        self.shaderScreenHeight = GL.glGetUniformLocation(self.program, "screenHeight")
        self.vertex_buffer = self.create_vertex_buffer()
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

    def draw(self):
        GL.glUseProgram(self.program)
        GL.glUniform1f(self.shaderScreenWidth, self.screen_size[0])
        GL.glUniform1f(self.shaderScreenHeight, self.screen_size[1])
        GL.glUniform1f(self.pixel_size_location, 0.025)
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
