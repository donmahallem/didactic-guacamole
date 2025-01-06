import glfw
import pygame
from OpenGL import GL
from OpenGL import GLU
from guacamole.constants import SCREEN_BASE_HEIGHT, SCREEN_BASE_WIDTH, KEY_DELTA_T
from base_game import BaseGame
from shaders import LightHouseShader


WINDOW_SIZE = (600, int(600 / SCREEN_BASE_WIDTH * SCREEN_BASE_HEIGHT))

WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE


def create_fbo(width, height):
    fbo = GL.glGenFramebuffers(1)
    GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, fbo)
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        GL.GL_RGB,
        width,
        height,
        0,
        GL.GL_RGB,
        GL.GL_UNSIGNED_BYTE,
        None,
    )
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glFramebufferTexture2D(
        GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, texture, 0
    )
    rbo = GL.glGenRenderbuffers(1)
    GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, rbo)
    GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH24_STENCIL8, width, height)
    GL.glFramebufferRenderbuffer(
        GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_RENDERBUFFER, rbo
    )
    if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError("Framebuffer is not complete")
    GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
    return fbo, texture


clock = pygame.time.Clock()


def main():
    # Initialize the library
    if not glfw.init():
        return

    # Create the first window
    window1 = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Window 1", None, None)
    if not window1:
        glfw.terminate()
        return

    # Create the second window
    window2 = glfw.create_window(
        WINDOW_WIDTH, WINDOW_WIDTH * 14 // 28, "Window 2", None, None
    )
    if not window2:
        glfw.terminate()
        return

    # Make the first window's context current
    glfw.make_context_current(window1)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
    basegame = BaseGame(SCREEN_BASE_WIDTH, SCREEN_BASE_HEIGHT)
    glfw.make_context_current(window2)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
    pixel_shader = LightHouseShader((WINDOW_WIDTH, WINDOW_WIDTH * 14 // 28))
    glfw.make_context_current(window1)
    fbo, fbo_texture = create_fbo(WINDOW_WIDTH, WINDOW_HEIGHT)
    # Loop until the user closes the window
    while not glfw.window_should_close(window1) and not glfw.window_should_close(
        window2
    ):
        # Render here, e.g. using pyOpenGL
        deltaT = clock.tick()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, fbo)
        # GL.glViewport(0, 0, 800, 600)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, SCREEN_BASE_WIDTH, 0, SCREEN_BASE_HEIGHT)
        basegame.update(**{KEY_DELTA_T: deltaT})
        basegame.draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

        glfw.make_context_current(window1)
        # GL.glViewport(0, 0, 800, 600)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBindTexture(GL.GL_TEXTURE_2D, fbo_texture)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0, 0)
        GL.glVertex2f(-1, -1)
        GL.glTexCoord2f(1, 0)
        GL.glVertex2f(1, -1)
        GL.glTexCoord2f(1, 1)
        GL.glVertex2f(1, 1)
        GL.glTexCoord2f(0, 1)
        GL.glVertex2f(-1, 1)
        GL.glEnd()
        glfw.swap_buffers(window1)

        glfw.make_context_current(window2)
        # GL.glViewport(0, 0, 800, 300)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBindTexture(GL.GL_TEXTURE_2D, fbo_texture)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0, 0)
        GL.glVertex2f(-1, -1)
        GL.glTexCoord2f(1, 0)
        GL.glVertex2f(1, -1)
        GL.glTexCoord2f(1, 1)
        GL.glVertex2f(1, 1)
        GL.glTexCoord2f(0, 1)
        GL.glVertex2f(-1, 1)
        GL.glEnd()
        # pixel_shader.draw()
        # Swap front and back buffers
        glfw.swap_buffers(window2)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
