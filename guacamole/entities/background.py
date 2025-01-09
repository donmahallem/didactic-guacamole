from OpenGL import GL
from guacamole.constants import SCREEN_BASE_HEIGHT, SCREEN_BASE_WIDTH, KEY_MOUSE_POS
from .sprite import Sprite
from guacamole.shaders.util import create_shader_program
import glm

VERTEX_BUFFER = 0
COLOR_BUFFER = 1


vertex_shader = f"""
#version 330 core
layout (location = 0) in vec3 aPos; // the position variable has attribute position 0
layout(location = 1) in vec2 aTexCoord;
uniform vec2 mousePosition;
uniform vec2 resolution;

out vec2 TexCoords;

void main()
{{
    gl_Position = vec4(aPos, 1.0); // see how we directly give a vec3 to vec4's constructor
    TexCoords = aTexCoord;
}}
"""
fragment_shader = f"""
#version 330 core
out vec4 FragColor;
in vec2 TexCoords;

uniform vec2 mousePosition;
uniform vec2 resolution;

void main()
{{
    vec2 uv = mousePosition / resolution;
    float red = fract(TexCoords.x+mousePosition.x);///resolution.x;
    float green = fract(TexCoords.y+mousePosition.y);///resolution.y;
    FragColor = vec4(red,green, 0.0, 1.0);
}} 
"""


class GradientBackground(Sprite):
    def __init__(self, size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)):
        self._size = size
        print(size)
        self._mousePosition = glm.vec2(0, 0)
        self._shader = create_shader_program(vertex_shader, fragment_shader)
        self._shaderParamResolution = GL.glGetUniformLocation(
            self._shader, "resolution"
        )
        self._shaderParamMousePosition = GL.glGetUniformLocation(
            self._shader, "mousePosition"
        )

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        if KEY_MOUSE_POS in kwargs:
            self.mousePosition = kwargs[KEY_MOUSE_POS]

    @property
    def mousePosition(self) -> glm.vec2:
        return self._mousePosition

    @mousePosition.setter
    def mousePosition(self, pos: glm.vec2) -> None:
        if isinstance(pos, glm.vec2):
            self._mousePosition.xy = pos.xy
        elif isinstance(pos, tuple) and len(pos) == 2:
            self._mousePosition.xy = pos

    def draw(self):
        GL.glUseProgram(self._shader)
        GL.glUniform2f(
            self._shaderParamMousePosition,
            self._mousePosition[0],
            self._mousePosition[1],
        )
        GL.glUniform2f(self._shaderParamResolution, self._size[0], self._size[1])

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
        GL.glUseProgram(0)
