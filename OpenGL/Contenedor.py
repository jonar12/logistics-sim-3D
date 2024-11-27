from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Contenedor:
    def __init__(self, body, pos, color):
        self.position = pos
        self.body = body
        self.color = color
        self.display_list = self.create_display_list()

    # Método para mover el contenedor hacia adelante
    def forward(self):
        self.position[2] += -1 
        
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
        glTexCoord(0, 0)
        glVertex3f(0.0, 0.0, 0.0)
        glTexCoord(1, 0)
        glVertex3f(0.0, point1, 0.0)
        glTexCoord(1, 1)
        glVertex3f(0.0, point1, point2)
        glTexCoord(0, 1)
        glVertex3f(0.0, 0.0, point2)

        # Cara trasera
        glTexCoord(0, 0)
        glVertex3f(point, 0.0, 0.0)
        glTexCoord(1, 0)
        glVertex3f(point, point1, 0.0)
        glTexCoord(1, 1)
        glVertex3f(point, point1, point2)
        glTexCoord(0, 1)
        glVertex3f(point, 0.0, point2)
        
        # Cara superior
        glTexCoord(0, 0)
        glVertex3f(0.0, point1, 0.0)
        glTexCoord(1, 0)
        glVertex3f(point, point1, 0.0)
        glTexCoord(1, 1)
        glVertex3f(point, point1, point2)
        glTexCoord(0, 1)
        glVertex3f(0.0, point1, point2)

        # Cara inferior
        glTexCoord(0, 0)
        glVertex3f(0.0, 0.0, 0.0)
        glTexCoord(1, 0)
        glVertex3f(point, 0.0, 0.0)
        glTexCoord(1, 1)
        glVertex3f(point, 0.0, point2)
        glTexCoord(0, 1)
        glVertex3f(0.0, 0.0, point2)
        
        # Cara lateral izquierda
        glTexCoord(0, 0)
        glVertex3f(0.0, 0.0, 0.0)
        glTexCoord(1, 0)
        glVertex3f(0.0, point1, 0.0)
        glTexCoord(1, 1)
        glVertex3f(point, point1, 0.0)
        glTexCoord(0, 1)
        glVertex3f(point, 0.0, 0.0)

        # Cara lateral derecha
        glTexCoord(0, 0)
        glVertex3f(0.0, 0.0, point2)
        glTexCoord(1, 0)
        glVertex3f(0.0, point1, point2)
        glTexCoord(1, 1)
        glVertex3f(point, point1, point2)
        glTexCoord(0, 1)
        glVertex3f(point, 0.0, point2)

        glEnd()

        glEndList()
        return display_list
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScaled(1.0, 1.0, 1.0)

        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)

        # Dibujar el camión usando la lista de despliegue
        glCallList(self.display_list)

        glPopMatrix()

