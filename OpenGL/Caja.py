from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Caja:
    def __init__(self, pos, final_pos, body, color):
        # Se inicializa las coordenadas de los vertices del cubo
        self.position = [pos[0], -8.5, pos[2]]
        self.final_pos = final_pos
        self.body = body
        self.color = color
        self.is_being_carried = False
        self.angle = 0 # Ángulo de rotación de la caja
        self.angle_montacarga = 0

    def returnToFinalPosition(self):
        initialPosX, _, initialPosZ = self.position
        finalPosX, _, finalPosZ = self.final_pos
        if initialPosX == finalPosX and initialPosZ  == finalPosZ:
            self.position = self.final_pos

    def setPosition(self, pos):
        self.position = [pos[0], -8.5, pos[2]]

    def getPosition(self):
        return self.position
    
    def setBeingCarried(self, is_being_carried, angle_montacarga=None):
        self.is_being_carried = is_being_carried
        self.angle_montacarga = angle_montacarga
    
    def update_position_y(self):
        if self.is_being_carried:
            self.position[1] = -5.6

    def setAngle(self, angle):
        self.angle = angle
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        if self.is_being_carried and self.angle_montacarga is not None:
            glRotatef(self.angle_montacarga, 0.0, 1.0, 0.0)

        # Dibujamos la caja
        self.drawBox()

        glPopMatrix()

    def drawBox(self):
        glPushMatrix()
        glTranslatef(self.body[0] / 2, 0.0, self.body[2] / 2)
        glColor3f(*self.color)

        glBegin(GL_QUADS)

        # Dimensiones de la caja
        width, height, depth = self.body

        # Cara frontal
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(width, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(width, height, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.0, height, 0.0)

        # Cara trasera
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.0, 0.0, depth)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(width, 0.0, depth)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(width, height, depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.0, height, depth)

        # Cara i0.0quierda
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.0, 0.0, depth)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.0, height, depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.0, height, 0.0)

        # Cara derecha
        glTexCoord2f(0.0, 0.0)
        glVertex3f(width, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(width, 0.0, depth)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(width, height, depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(width, height, 0.0)

        # Cara superior
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.0, height, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(width, height, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(width, height, depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.0, height, depth)

        # Cara inferior
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(width, 0.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(width, 0.0, depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.0, 0.0, depth)

        glEnd()
        glPopMatrix()