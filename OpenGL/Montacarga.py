from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Montacarga:
    def __init__(self, pos, angle, obj, materiales):
        self.materiales = materiales
        self.position = [pos[0] + 2.5, 0.0, pos[2] + 2.5]
        # self.position = [pos[0], 18.5, pos[2]]
        self.angle = angle
        self.scene = obj
        self.target_angle = angle
        self.is_rotating = False
        self.next_position = self.position
        self.rotation_speed = 1.0
        self.display_list = self.create_display_list()

    # def setPosition(self, pos):
    #     self.position = [pos[0] + 0.5, 0, pos[2] + 14.5]
    def setPosition(self, pos):
        self.next_position = [pos[0] + 2.5, 0, pos[2] + 2.5]

    def getPosition(self):
        return self.position
    
    def isRotating(self):
        return self.is_rotating

    def setTargetAngle(self, angle):
        # Asegurarse de que el ángulo esté entre 0 y 360
        self.target_angle = angle % 360

        # El montacarga está rotando
        self.is_rotating = True

    def update(self):
        angle_diff = (self.target_angle - self.angle + 180) % 360 - 180

        # Ajustar el ángulo actual hacia el ángulo objetivo
        if abs(angle_diff) > self.rotation_speed:
            self.angle += self.rotation_speed * (1 if angle_diff > 0 else -1)
            self.angle %= 360
        else:
            self.angle = self.target_angle
            self.is_rotating = False
            self.position = self.next_position

    def create_display_list(self):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)

        # Dibujar el Montacarga
        for _, mesh in self.scene.meshes.items():
            for i, face in enumerate(mesh.faces):
                material_obj = mesh.materials[i % len(mesh.materials)]
                material_name = material_obj.name
                color_diffuso = self.materiales.get(material_name, {}).get('Kd', [1.0, 1.0, 1.0])
                glColor3f(*color_diffuso)

                glBegin(GL_TRIANGLES)
                for vertex_i in face:
                    vertex = self.scene.vertices[vertex_i]
                    glVertex3f(*vertex)
                glEnd()
        glEndList()
        return display_list

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.angle, 0.0, 1.0, 0.0)
        # glScaled(0.085, 0.085, 0.085)
        glScaled(0.04, 0.04, 0.04)
        
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)

        # Dibujar el Montacarga usando la lista de visualización
        glCallList(self.display_list)

        glPopMatrix()