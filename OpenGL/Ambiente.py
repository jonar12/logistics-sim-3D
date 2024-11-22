from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Ambiente:
    def __init__(self, pos, scale, obj, materiales, angle, rotAxis):
        self.scale = scale
        self.position = pos
        self.angle = angle
        self.rotAxis = rotAxis
        self.materiales = materiales
        self.scene = obj
        self.display_list = self.create_display_list()
        
    def create_display_list(self):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)

        # Dibujar objetos para decorar el ambiente
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
        glRotatef(self.angle, self.rotAxis[0], self.rotAxis[1], self.rotAxis[2])
        glScaled(self.scale[0], self.scale[1], self.scale[2])

        # Dibujar objetos para decorar el ambiente usando la lista de despliegue
        glCallList(self.display_list)
        glPopMatrix()

