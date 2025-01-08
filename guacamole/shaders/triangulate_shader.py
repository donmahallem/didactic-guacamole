from OpenGL import GL
from .base_shader import BaseShader

vertex_shader_identy = """
#version 330
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragment_shader_triangles = """
#version 330 core

uniform sampler2D screenTexture;
uniform float pixelSize;
uniform float screenHeight;
uniform float screenWidth;
out vec4 FragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(screenWidth, screenHeight);
    vec2 sliceCoord = floor(uv / pixelSize) * pixelSize;
    vec2 offset = mod(uv, pixelSize);

    vec4 color1 = texture(screenTexture, sliceCoord);
    vec4 color2 = texture(screenTexture, sliceCoord + vec2(pixelSize, 0.0));
    vec4 color3 = texture(screenTexture, sliceCoord + vec2(0.0, pixelSize));
    vec4 color4 = texture(screenTexture, sliceCoord + vec2(pixelSize, pixelSize));

    vec4 averageColor;
    if (offset.x + offset.y < pixelSize) {
        averageColor = (color1 + color2 + color3) / 3.0;
    } else {
        averageColor = (color2 + color3 + color4) / 3.0;
    }

    FragColor = averageColor;
}
"""


class TriangulateShader(BaseShader):
    def __init__(self, screen_size):
        super().__init__(vertex_shader_identy, fragment_shader_triangles, screen_size)
        self.pixel_size_location = GL.glGetUniformLocation(self.program, "pixelSize")

    def drawSetup(self):
        GL.glUniform1f(self.pixel_size_location, 0.025)
        super().drawSetup()
