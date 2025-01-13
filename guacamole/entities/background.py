from OpenGL import GL
from guacamole.constants import (
    SCREEN_BASE_HEIGHT,
    SCREEN_BASE_WIDTH,
    KEY_MOUSE_POS,
    KEY_DELTA_T,
)
from .sprite import Sprite
from guacamole.shaders.util import create_shader_program
import glm
import math

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
uniform vec2 timeOffset;

void main()
{{
    vec2 uv = TexCoords;
    float red = pos.x+mousePosition.x+timeOffset.x;
    float green = pos.y+mousePosition.y+timeOffset.y;
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
    FragColor = vec4(red,green, blue,0.8);
}} 
"""


class GradientBackground(Sprite):
    def __init__(self, size=(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)):
        super().__init__()
        self._size = size
        self._mousePosition = glm.vec2(0, 0)
        self._shader = create_shader_program(vertex_shader, fragment_shader)
        self._shaderParamResolution = GL.glGetUniformLocation(
            self._shader, "resolution"
        )
        self._shaderParamMousePosition = GL.glGetUniformLocation(
            self._shader, "mousePosition"
        )
        self._shaderParamTimeOffset = GL.glGetUniformLocation(
            self._shader, "timeOffset"
        )
        self._animTime = 0

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        if KEY_MOUSE_POS in kwargs:
            self.mousePosition = kwargs[KEY_MOUSE_POS]
        if KEY_DELTA_T in kwargs:
            self._animTime += kwargs[KEY_DELTA_T]

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
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glUseProgram(self._shader)
        GL.glUniform2f(
            self._shaderParamMousePosition,
            self._mousePosition[0],
            self._mousePosition[1],
        )
        GL.glUniform2f(self._shaderParamResolution, self._size[0], self._size[1])
        GL.glUniform2f(
            self._shaderParamTimeOffset,
            math.sin(self._animTime / 2),
            math.cos(math.sqrt(self._animTime)) * 3,
        )
        GL.glPushMatrix()
        GL.glTranslatef(self.position.x, self.position.y, self.position.z)
        GL.glBegin(GL.GL_QUADS)
        # GL.glColor3f(1.0, 0.0, 0.0)  # Red
        GL.glVertex3f(-1, -1, 0)
        # GL.glColor3f(0.0, 1.0, 0.0)  # Green
        GL.glVertex3f(1, -1, 0)
        # GL.glColor3f(0.0, 0.0, 1.0)  # Blue
        GL.glVertex3f(1, 1, 0)
        # GL.glColor3f(1.0, 1.0, 0.0)  # Yellow
        GL.glVertex3f(-1, 1, 0)
        GL.glEnd()
        GL.glPopMatrix()
        GL.glUseProgram(0)
        GL.glDisable(GL.GL_BLEND)
