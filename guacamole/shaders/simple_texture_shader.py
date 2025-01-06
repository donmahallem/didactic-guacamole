import numpy as np
from OpenGL import GL
from .util import create_shader_program

vertex_shader = """
#version 330
layout(location = 0) in vec2 position;
layout(location = 1) in vec2 texCoord;
out vec2 TexCoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    TexCoord = texCoord;
}
"""

fragment_shader = """
#version 330
in vec2 TexCoord;
out vec4 fragColor;
uniform sampler2D screenTexture;
void main()
{
    fragColor = texture(screenTexture, TexCoord);
}
"""

vertices = np.array(
    [
        # Positions    # TexCoords
        -1.0,
        1.0,
        0.0,
        1.0,
        -1.0,
        -1.0,
        0.0,
        0.0,
        1.0,
        -1.0,
        1.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ],
    dtype=np.float32,
)

indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)


def createSimpleTextureShader():
    vao = GL.glGenVertexArrays(1)
    vbo = GL.glGenBuffers(1)
    ebo = GL.glGenBuffers(1)

    GL.glBindVertexArray(vao)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo)
    GL.lBufferData(
        GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW
    )

    # Position attribute
    GL.glVertexAttribPointer(
        0, 2, GL.GL_FLOAT, GL.GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0)
    )
    GL.glEnableVertexAttribArray(0)

    # Texture coordinate attribute
    GL.glVertexAttribPointer(
        1,
        2,
        GL.GL_FLOAT,
        GL.GL_FALSE,
        4 * vertices.itemsize,
        ctypes.c_void_p(2 * vertices.itemsize),
    )
    GL.glEnableVertexAttribArray(1)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindVertexArray(0)
