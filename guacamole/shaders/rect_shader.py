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
#version 330 core

uniform sampler2D screenTexture;
uniform float sampleOffsetX;
uniform float sampleOffsetY;
uniform int numSamples;
out vec4 FragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / textureSize(screenTexture,0);
    vec2 sliceCoord = floor(uv / vec2(sampleOffsetX, sampleOffsetY)) * vec2(sampleOffsetX, sampleOffsetY);

    vec4 color = vec4(0.0);
    for (int i = 0; i < numSamples; i++) {
        for (int j = 0; j < numSamples; j++) {
            vec2 offset = vec2(float(i) / float(numSamples) * sampleOffsetX, float(j) / float(numSamples) * sampleOffsetY);
            color += texture(screenTexture, sliceCoord + offset);
        }
    }
    color /= float(numSamples * numSamples);

    FragColor = color;
}
"""


class RectShader(BaseShader):
    def __init__(self, screen_size):
        super().__init__(vertex_shader_identy, fragment_shader_squares, screen_size)
        self.shaderNumSamples = GL.glGetUniformLocation(self.program, "numSamples")
        self.shaderSampleOffsetY = GL.glGetUniformLocation(
            self.program, "sampleOffsetY"
        )
        self.shaderSampleOffsetX = GL.glGetUniformLocation(
            self.program, "sampleOffsetX"
        )
        self._shaderSamples = 4

    def setShaderSamples(self, samples):
        if samples < 1:
            raise ValueError(f"Samples should be atleast 1")
        self._shaderSamples = int(samples)

    def drawSetup(self):
        GL.glUniform1i(self.shaderNumSamples, self._shaderSamples)
        GL.glUniform1f(self.shaderSampleOffsetX, 0.01)
        GL.glUniform1f(self.shaderSampleOffsetY, 0.02)
        super().drawSetup()
