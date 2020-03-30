from src.engine.Camera import Camera

import glm
import ctypes
import pygame
import numpy
from pygame.constants import *
from OpenGL import GL
from OpenGL.GL import shaders
from OpenGL.raw.GL import _types

class Test():
    def start_test(self):
        pygame.init()
        pygame.display.set_mode((600, 400), DOUBLEBUF | OPENGL)
        playing = True
        timer = pygame.time.Clock()
        GL.glClearColor(0.1, 0.1, 0.1, 1)

        #create camera
        camera = Camera(600, 400, glm.vec3(0, 0, 0))

        #create mesh data
        vertex_data = numpy.array([
                -0.5, -0.5,  0.0, 1.0, 1.0, 1.0, 0.0, 0.0,
                0.5, -0.5,  0.0, 1.0, 1.0, 1.0, 1.0, 0.0,
                0.5,  0.5,  0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                -0.5,  0.5,  0.0, 1.0, 1.0, 1.0, 0.0, 1.0,
            ], dtype=numpy.float32)

        index_data = numpy.array([
        0, 1, 2,
        2, 3, 0,
        ], dtype=numpy.uint32)

        #create texture
        img = pygame.image.load("data/textures/tile_floor.png").convert()
        w, h = img.get_size()
        texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        texture_info = pygame.image.tostring(img, "RGBA", 1)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, 4, w, h, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, texture_info)

        VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(VAO)

        VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL.GL_STATIC_DRAW)

        EBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, (8 * ctypes.sizeof(_types.GLfloat)), None)
        GL.glEnableVertexAttribArray(0)

        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, (8 * ctypes.sizeof(_types.GLfloat)),
                                 ctypes.c_void_p((3 * ctypes.sizeof(_types.GLfloat))))
        GL.glEnableVertexAttribArray(1)

        GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, (8 * ctypes.sizeof(_types.GLfloat)),
                                 ctypes.c_void_p((6 * ctypes.sizeof(_types.GLfloat))))
        GL.glEnableVertexAttribArray(2)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

        # Generate shaders
        vertex_shader = shaders.compileShader("""
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aColor;
        layout (location = 2) in vec2 aTexCoord;

        out vec3 ourColor;
        out vec2 TexCoord;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
            ourColor = aColor;
            TexCoord = aTexCoord;
        }
        """,
        GL.GL_VERTEX_SHADER)
        '''
        vertex_shader = GL.shaders.compileShader("""
            #version 330 core
            layout (location = 0) in vec3 aPos;
            layout (location = 1) in vec3 aColor;
            layout (location = 2) in vec2 aTexCoord;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main() {
                gl_Position = vec4(aPos, 1.0);
            }
            """,
                                              GL.GL_VERTEX_SHADER)
        '''
        fragment_shader = GL.shaders.compileShader("""
        #version 330 core
        out vec4 FragColor;

        in vec3 ourColor;
        in vec2 TexCoord;

        uniform sampler2D ourTexture;

        void main()
        {
            FragColor = texture(ourTexture, TexCoord) * vec4(ourColor, 1.0);
        }
        """, GL.GL_FRAGMENT_SHADER)
        shader = GL.shaders.compileProgram(vertex_shader, fragment_shader)

        while playing:
            dt = 0.001 * timer.tick(60)
            for event in pygame.event.get():
                if event.type in (MOUSEBUTTONDOWN, KEYDOWN):
                    playing = False

            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            model_transform = glm.mat4()
            model_transform = glm.translate(model_transform , glm.vec3(0.0, 0.0, -2.0))
            GL.shaders.glUseProgram(shader)

            GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

            transform_loc = GL.glGetUniformLocation(shader, "model")
            GL.glUniformMatrix4fv(transform_loc, 1, GL.GL_FALSE, glm.value_ptr(model_transform))

            view_loc = GL.glGetUniformLocation(shader, "view")
            GL.glUniformMatrix4fv(view_loc, 1, GL.GL_FALSE, glm.value_ptr(camera.get_view_matrix()))

            projection_loc = GL.glGetUniformLocation(shader, "projection")
            GL.glUniformMatrix4fv(projection_loc, 1, GL.GL_FALSE, glm.value_ptr(camera.get_projection_matrix()))

            #draw
            GL.glBindVertexArray(VAO)

            GL.glDrawElements(GL.GL_TRIANGLES, index_data.size, GL.GL_UNSIGNED_INT, None)

            GL.shaders.glUseProgram(0)
            GL.glBindVertexArray(0)

            pygame.display.flip()


if __name__ == "__main__":
    test = Test()
    test.start_test()
