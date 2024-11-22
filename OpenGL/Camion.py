from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Camion:
    def __init__(self, body, pos, color):
        self.posicion = pos
        self.body = body
        self.color = color
        self.display_list = self.create_display_list()
    
    def create_display_list(self):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)
        
        point = self.body[0]
        point1 = self.body[1]
        point2 = self.body[2]

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Dibujar el contenedor del camión
        glColor4f(*self.color, 0.5)
        glBegin(GL_QUADS)

        # Cara frontal
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.posicion[0], self.posicion[1], self.posicion[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.posicion[0], self.posicion[1] + point1, self.posicion[2])
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1] + point1, self.posicion[2])
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1], self.posicion[2])

        # Cara trasera
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.posicion[0], self.posicion[1], self.posicion[2] + point2)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.posicion[0], self.posicion[1] + point1, self.posicion[2] + point2)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1] + point1, self.posicion[2] + point2)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1], self.posicion[2] + point2)

        # Cara izquierda
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.posicion[0], self.posicion[1], self.posicion[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.posicion[0], self.posicion[1] + point1, self.posicion[2])
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.posicion[0], self.posicion[1] + point1, self.posicion[2] + point2)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.posicion[0], self.posicion[1], self.posicion[2] + point2)
        
        # Cara derecha
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1], self.posicion[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1] + point1, self.posicion[2])
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1] + point1, self.posicion[2] + point2)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1], self.posicion[2] + point2)

        # Cara superior
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.posicion[0], self.posicion[1] + point1, self.posicion[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.posicion[0], self.posicion[1] + point1, self.posicion[2] + point2)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1] + point1, self.posicion[2] + point2)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1] + point1, self.posicion[2])

        # Cara inferior
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.posicion[0], self.posicion[1], self.posicion[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.posicion[0], self.posicion[1], self.posicion[2] + point2)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1], self.posicion[2] + point2)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.posicion[0] + point, self.posicion[1], self.posicion[2])

        glEnd()

        glEndList()
        return display_list
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.posicion[0], self.posicion[1], self.posicion[2])
        glScaled(1.0, 1.0, 1.0)

        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)

        # Dibujar el camión usando la lista de despliegue
        glCallList(self.display_list)

        glPopMatrix()

