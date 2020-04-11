import ctypes

import glm
import numpy
import pygame
from OpenGL import GL
from OpenGL.GL import shaders
from OpenGL.raw.GL import _types

from src.application_base import ApplicationBase
from src.engine.pygame.camera import Camera


class PyGameApplication(ApplicationBase):
    def __init__(self, config):
        ApplicationBase.__init__(self, config)

        self.display_surface = None
        self.main_surface = None
        self.running = True
        self.is_initialized = False
        self.timer = pygame.time.Clock()
        self.delta_time = 0
        self.ticks_last_frame = 0

    def _create_render_texture(self):
        w, h = self.main_surface.get_size()
        self.game_texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.game_texture)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)

    def _use_pygame_texture(self):
        w, h = self.main_surface.get_size()
        texture_info = pygame.image.tostring(self.main_surface, "RGBA", 1)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, 4, w, h, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, texture_info)

    def _create_render_plane(self):
        self.vertex_data = numpy.array([
            -0.5, -0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,
            0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            -0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0,
        ], dtype=numpy.float32)

        self.index_data = numpy.array([
            0, 1, 2,
            2, 3, 0,
        ], dtype=numpy.uint32)

        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)

        self.VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data, GL.GL_STATIC_DRAW)

        self.EBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index_data.nbytes, self.index_data, GL.GL_STATIC_DRAW)

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

    def _create_shaders(self):
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
        self.shader = GL.shaders.compileProgram(vertex_shader, fragment_shader)

    def _render_game_texture(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        model_transform = glm.mat4()
        model_transform = glm.translate(model_transform, glm.vec3(0.0, 0.0, -1.0))
        GL.shaders.glUseProgram(self.shader)

        self._use_pygame_texture()
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.game_texture)

        transform_loc = GL.glGetUniformLocation(self.shader, "model")
        GL.glUniformMatrix4fv(transform_loc, 1, GL.GL_FALSE, glm.value_ptr(model_transform))

        view_loc = GL.glGetUniformLocation(self.shader, "view")
        GL.glUniformMatrix4fv(view_loc, 1, GL.GL_FALSE, glm.value_ptr(self.camera_3d.get_view_matrix()))

        projection_loc = GL.glGetUniformLocation(self.shader, "projection")
        GL.glUniformMatrix4fv(projection_loc, 1, GL.GL_FALSE, glm.value_ptr(self.camera_3d.get_ortogonal_matrix()))

        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index_data.size, GL.GL_UNSIGNED_INT, None)

        GL.shaders.glUseProgram(0)
        GL.glBindVertexArray(0)

    def _show_window(self):
        self.display_surface = pygame.display.set_mode(
            (self.application_config.window_width, self.application_config.window_height),
            pygame.constants.DOUBLEBUF | pygame.constants.OPENGL)

    def _init_engine(self):
        self.running = True
        pygame.init()
        pygame.display.set_caption(self.application_config.window_title)

        self._show_window()
        self.main_surface = pygame.Surface(( self.application_config.window_width,  self.application_config.window_height))

        GL.glClearColor(0.0, 0.6, 0.75, 1)
        self.camera_3d = Camera(self.application_config.window_width,  self.application_config.window_height, glm.vec3(0, 0, 0))

        self._create_render_plane()
        self._create_render_texture()
        self._create_shaders()

    def add_zoom(self, value):
        self.camera_3d.zoom += value
        self.main_surface = pygame.Surface(
            (self.application_config.window_width * 1/self.camera_3d.zoom, self.application_config.window_height * 1/self.camera_3d.zoom))

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def _update(self):
        ticks = pygame.time.get_ticks()
        self.delta_time = (ticks - self.ticks_last_frame) / 1000.0
        self.ticks_last_frame = ticks

    def _render(self):
        pass

    def _on_render(self):
        self.main_surface.fill((0, 0, 0))

        self._render()
        self._render_game_texture()

    def _cleanup(self):
        pygame.quit()

    def initialize(self):
        self._init_engine()
        self.is_initialized = True

    def start_game_loop(self):
        while self.running:
            self.timer.tick(60)
            self.game_loop()
            pygame.display.flip()
        self._cleanup()

    def game_loop(self):
        for event in pygame.event.get():
            self._on_event(event)

        self._update()
        self._on_render()


