from OpenGL import GL
from .base_shader import BaseShader

vertex_shader_identy = """
#version 330
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader_squares = """
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


class PixelateShader(BaseShader):
    def __init__(self, screen_size):
        super().__init__(vertex_shader_identy, fragment_shader_squares, screen_size)
        self.pixel_size_location = GL.glGetUniformLocation(self.program, "pixelSize")

    def drawSetup(self):
        GL.glUniform1f(self.pixel_size_location, 0.025)
        super().drawSetup()
