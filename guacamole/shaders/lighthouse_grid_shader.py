from pygame.locals import *
from OpenGL import GL
from .base_shader import BaseShader
import numpy as np
from guacamole.constants import (
    PIXEL_NUM_HORIZONTAL,
    PIXEL_NUM_VERTICAL,
    PIXEL_SIZE_HORIZONTAL,
    PIXEL_SIZE_VERTICAL,
    PIXEL_SPACING_HORIZONTAL,
    PIXEL_SPACING_VERTICAL,
    SCREEN_BASE_HEIGHT,
    SCREEN_BASE_WIDTH,
)

vertex_shader_identy = """
#version 330 core
layout(location = 0) in vec2 position;
out vec2 fragCoord;
void main() {
    fragCoord = position*0.5+0.5;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader_squares = f"""
#version 330 core

uniform sampler2D screenTexture;
uniform float gridSize;
uniform float screenHeight;
uniform float screenWidth;
in vec2 texCoord;
out vec4 FragColor;

void main() {{
    vec2 grid = fract(texCoord / vec2({SCREEN_BASE_WIDTH},{SCREEN_BASE_HEIGHT}));
    vec4 color = texture(screenTexture, grid);
    if (grid.x < 0.011 || grid.y < 0.037){{
        color = vec4(0.0, 0.0, 0.0, 1.0);
        // Grid lines color (black)
    }}
    FragColor = color;
}}
"""

vertex_shader_identy2 = """
#version 330
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragment_shader_squares = f"""
#version 330 core

uniform sampler2D screenTexture;
in vec2 fragCoord;
uniform vec2 resolution;
uniform vec2 lineWidth;
uniform vec2 cellCount;

out vec4 FragColor;

void main() {{
    vec2 uv = gl_FragCoord.xy / resolution;
    vec2 grid = fract(uv * cellCount);
    vec4 color = texture(screenTexture, uv);
    if (grid.x > 1-lineWidth.x*(cellCount.x-1) || grid.y >1- lineWidth.y*(cellCount.y-1)){{
        color = vec4(0.0, 0.0, 0.0, 1.0);
        // Grid lines color (black)
    }}
    FragColor = color;
}}

"""
fragment_shader_squares2 = f"""
#version 330 core

uniform sampler2D screenTexture;
in vec2 fragCoord;
uniform vec2 resolution;
uniform vec2 lineWidth;
uniform vec2 cellCount;

out vec4 FragColor;

void main() {{
    vec2 uv = gl_FragCoord.xy / resolution;
    vec2 grid = fract(uv * cellCount);
    vec4 color = texture(screenTexture, fragCoord);
    vec2 gridLine = step(grid, vec2(lineWidth.x / resolution.x, lineWidth.y / resolution.y)) + step(1.0 - grid, vec2(lineWidth.x / resolution.x, lineWidth.y / resolution.y));
    float line = max(gridLine.x, gridLine.y);
    FragColor = mix(color,vec4(0.0, 0.0, 0.0, 1.0),line);
}}

"""


class LightHouseGridShader(BaseShader):
    def __init__(self, screen_size):
        super().__init__(vertex_shader_identy, fragment_shader_squares2, screen_size)
        self.shaderResolution = GL.glGetUniformLocation(self.program, "resolution")
        self.shaderLineWidth = GL.glGetUniformLocation(self.program, "lineWidth")
        self.shaderCellCount = GL.glGetUniformLocation(self.program, "cellCount")

    def drawSetup(self):
        GL.glUniform2f(self.shaderResolution, self.screen_size[0], self.screen_size[1])
        GL.glUniform2f(
            self.shaderLineWidth, PIXEL_SPACING_HORIZONTAL, PIXEL_SPACING_VERTICAL
        )
        GL.glUniform2f(
            self.shaderCellCount, PIXEL_NUM_HORIZONTAL * 1.0, PIXEL_NUM_VERTICAL * 1.0
        )
        super().drawSetup()
