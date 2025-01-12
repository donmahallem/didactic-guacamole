from OpenGL import GL
from guacamole.constants import SCREEN_BASE_HEIGHT, SCREEN_BASE_WIDTH, KEY_MOUSE_POS
from .sprite import Sprite
from guacamole.shaders.util import create_shader_program
from guacamole.util.load_obj import loadObj
import ctypes
import glm
import numpy as np
import pywavefront

VERTEX_BUFFER = 0
COLOR_BUFFER = 1


vertex_shader = f"""
#version 330 core
layout (location = 0) in vec3 aPos; // the position variable has attribute position 0
layout(location = 1) in vec2 aTexCoord;
uniform vec2 mousePosition;
uniform vec2 resolution;

out vec2 TexCoords;
out vec3 pos;

void main()
{{
    gl_Position = vec4(aPos, 1.0); // see how we directly give a vec3 to vec4's constructor
    TexCoords = aTexCoord;
    pos=aPos*0.5+0.5;
    pos.x=1-pos.x;
}}
"""
fragment_shader = f"""
#version 330 core
out vec4 FragColor;
in vec2 TexCoords;
in vec3 pos;

uniform vec2 mousePosition;
uniform vec2 resolution;

void main()
{{
    vec2 uv = TexCoords;
    float red = pos.x+mousePosition.x;
    float green = pos.y+mousePosition.y;
    if(mod(red,2)>=1){{
        red=1-fract(red);
    }}else{{
        red=fract(red);
    }}
    if(mod(green,2)>=1){{
        green=1-fract(green);
    }}else{{
        green=fract(green);
    }}
    float blue = 1.0-max(red,green);
    FragColor = vec4(red,green, blue, 1.0);
}} 
"""


class Box(Sprite):
    def __init__(self, size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)):
        self._size = size
        self._vertices = loadObj("./guacamole/util/box.obj")
        self._vertices = np.array(self._vertices, dtype=np.float32)
        self._vertexCount = self._vertices.shape[0] // 8
        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)
        self._vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices, GL.GL_STATIC_DRAW
        )
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 32, ctypes.c_void_p(0))
        # GL.glEnableVertexAttribArray(1)
        # GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,32,ctypes.c_void_p(12))
        GL.glBindVertexArray(0)
        self._shader = create_shader_program(vertex_shader, fragment_shader)

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

    def draw(self) -> None:
        """
        Draw the triangle.
        """
        GL.glPushMatrix()
        GL.glLoadIdentity()
        # Translate to the center of the screen
        GL.glTranslatef(0.0, 0.0, -5.0)
        # Apply rotation and scaling
        # GL.glRotatef(rotation_angle, 0.0, 1.0, 0.0)
        GL.glScalef(20, 20, 20)
        GL.glUseProgram(self._shader)
        GL.glBindVertexArray(self._vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertexCount)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        GL.glPopMatrix()

    def destroy(self) -> None:
        """
        Free any allocated memory.
        """

        GL.glDeleteVertexArrays(1, (self._vao))
        GL.glDeleteBuffers(1, (self._vbo))


class Entity:
    def __init__(self, obj_file):
        self.obj = pywavefront.Wavefront(obj_file, collect_faces=True)
        self._pos = glm.vec3(0)
        self._scale = glm.vec3(1)

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, pos):
        self._pos = glm.vec3(pos)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = glm.vec3(scale)

    def draw(self):
        GL.glPushMatrix()
        GL.glTranslatef(*self.position)
        GL.glScalef(*self._scale)
        GL.glRotatef()
        GL.glBegin(GL.GL_TRIANGLES)
        for mesh in self.obj.mesh_list:
            for face in mesh.faces:
                for vertex_i in face:
                    GL.glVertex3fv(self.obj.vertices[vertex_i])
        GL.glEnd()
        GL.glPopMatrix()

    def update(self, *args, **kwargs):
        pass
