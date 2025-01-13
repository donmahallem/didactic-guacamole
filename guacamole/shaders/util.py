from OpenGL import GL
from PIL import Image
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


def loadTexture(path):
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        GL.GL_RGB,
        image.width,
        image.height,
        0,
        GL.GL_RGB,
        GL.GL_UNSIGNED_BYTE,
        img_data,
    )
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    return texture


def loadTextureGrey(path):
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        1,
        image.width,
        image.height,
        0,
        GL.GL_RED,
        GL.GL_UNSIGNED_BYTE,
        img_data,
    )
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    return texture
