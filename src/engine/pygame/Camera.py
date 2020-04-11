import glm

class Camera():

    def __init__(self, windows_width, windows_height, position):

        self.windows_width = float(windows_width)
        self.windows_height = float(windows_height)

        self.position = position
        self.world_up = glm.vec3(0.0, 1.0, 0.0)
        self.up = glm.vec3()
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3()

        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 10.0
        self.sensitivity = 0.1
        self.fov = 45.0

        self.zoom = 1.0

        self._update_camera_vectors()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.fov), self.windows_width / self.windows_height, -1, 1)

    def get_ortogonal_matrix(self):
        return glm.ortho(-0.5 * 1.0, 0.5 * 1.0, -0.5 * 1.0, 0.5 * 1.0)

    def _update_camera_vectors(self):
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))

        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))
