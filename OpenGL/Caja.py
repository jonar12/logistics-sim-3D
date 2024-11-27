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
        self.is_it_in_its_final_pos = False
        self.angle = 0 # Ángulo de rotación de la caja
        self.angle_montacarga = 0
        self.carrier = None # Hace referencia al Montacarga

    def returnToFinalPosition(self):
        initialPosX, _, initialPosZ = self.position
        finalPosX, _, finalPosZ = self.final_pos
        if initialPosX == finalPosX and initialPosZ  == finalPosZ:
            self.position = self.final_pos
            self.is_it_in_its_final_pos = True

    def setPosition(self, pos):
        self.position = [pos[0], -8.5, pos[2]]

    def getPosition(self):
        return self.position
    
    def setBeingCarried(self, is_being_carried, carrier=None):
        self.is_being_carried = is_being_carried
        self.carrier = carrier
        if carrier is not None:
            self.angle_montacarga = carrier.getAngle()
        else:
            self.carrier = None
            self.angle_montacarga = None
            self.angle = 0
    
    def update_position_y(self):
        if self.is_being_carried:
            self.position[1] = -5.6

    def setAngle(self, angle):
        self.angle = angle
    
    def draw(self):
        glPushMatrix()
        if self.is_being_carried and self.angle_montacarga is not None and self.carrier is not None:
            # Obtener la posición y el ángulo del montacargas
            carrier_pos = self.carrier.getPosition()
            carrier_angle = self.carrier.getAngle()

            # Trasladar a la posición del montacargas
            glTranslatef(carrier_pos[0], carrier_pos[1], carrier_pos[2])

            # Aplicar la rotación del montacargas
            glRotatef(carrier_angle, 0.0, 1.0, 0.0)

            # Verificar el tamaño de la caja para ajustar la posición
            match self.body[0]:
                case 1.0:
                    # Ajuste de la posición de la caja de tamaño 1.0
                    glTranslatef(-3.5, self.position[1], 9.0)
                case 5.0:
                    # Ajuste de la posición de la caja de tamaño 5.0
                    glTranslatef(-5.0, self.position[1], 8.0)
                case 7.0:
                    # Ajuste de la posición de la caja de tamaño 7.0
                    glTranslatef(-7.0, self.position[1], 5.8)
        else:
            # Si la caja no está siendo llevada, usar su posición normal
            glTranslatef(self.position[0], self.position[1], self.position[2])
            glRotatef(self.angle, 0.0, 1.0, 0.0)

        # Dibujar la caja centrada en el origen
        self.drawBox()
        glPopMatrix()

    def drawBox(self):
        glPushMatrix()
        if not self.is_it_in_its_final_pos:
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