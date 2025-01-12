from .sprite import Sprite
from OpenGL import GL
from guacamole.constants import KEY_DELTA_T
from guacamole.shaders.util import loadTexture
from OpenGL.GL.shaders import compileProgram, compileShader

vertex_shader = f"""
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 aTexCoords;
out vec2 TexCoords;
out vec3 pos;

void main()
{{
    gl_Position = vec4(aPos, 1.0); 
    pos=aPos;
    TexCoords = aTexCoords/200;
}}
"""
fragment_shader = f"""
#version 330 core
in vec2 TexCoords;
out vec4 color;
in vec3 pos;

uniform sampler2D texture1;
void main()
{{
    vec2 uv = TexCoords;
    color = vec4(pos.x,pos.y*uv.y/uv.x, 1.0, 1.0);
}} 
"""


class Water(Sprite):

    def __init__(self, size, parent=None):
        super().__init__(parent)
        self._size = size
        self._time = 0
        self._waterTexture = loadTexture("./assets/water.png")
        self._shader = compileProgram(
            compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER),
        )

    @property
    def width(self) -> float:
        return self._size[0]

    @property
    def height(self) -> float:
        return self._size[1]

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        if KEY_DELTA_T in kwargs:
            self._time += kwargs[KEY_DELTA_T]

    def draw(self):
        GL.glUseProgram(self._shader)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._waterTexture)
        GL.glPushMatrix()
        GL.glTranslatef(self.x, self.y, self.z)
        GL.glScalef(self.width * 5, self.height, 1)
        GL.glBegin(GL.GL_QUADS)
        # GL.glColor3f(1.0, 0.0, 0.0)  # Red
        GL.glVertex2f(-1, -1)
        # GL.glColor3f(0.0, 1.0, 0.0)  # Green
        GL.glVertex2f(1, -1)
        # GL.glColor3f(0.0, 0.0, 1.0)  # Blue
        GL.glVertex2f(1, 1)
        # GL.glColor3f(1.0, 1.0, 0.0)  # Yellow
        GL.glVertex2f(-1, 1)
        GL.glEnd()
        GL.glPopMatrix()
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)
