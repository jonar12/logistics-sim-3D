import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math


class Caja:
    def __init__(self, dim, vel, textures, txtIndex, pos, body, color):
        # Se inicializa las coordenadas de los vertices del cubo
        self.color = color
        self.body = body

        self.dim = dim
        self.position = [pos[0], 0, pos[2]]

        # Inicializar las coordenadas (x,y,z) del cubo en el tablero
        # almacenandolas en el vector position
        # ...
        # Se inicializa un vector de direccion aleatorio
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        magnitude = math.sqrt(dirX * dirX + dirZ * dirZ) * vel
        self.direction = [dirX / magnitude, 0, dirZ / magnitude]
        # El vector aleatorio debe de estar sobre el plano XZ (la altura en Y debe ser fija)
        # Se normaliza el vector de direccion
        # ...
        # Se cambia la maginitud del vector direccion con la variable vel
        # ...
        
        #Arreglo de texturas
        self.textures = textures

        #Index de la textura a utilizar
        self.txtIndex = txtIndex

        #Control variable for drawing
        self.alive = True

    # def update(self):
    #     # Se debe de calcular la posible nueva posicion del cubo a partir de su
    #     # posicion acutual (position) y el vector de direccion (direction)
    #     # ...
    #     newX = self.position[0] + self.direction[0]
    #     newZ = self.position[2] + self.direction[2]
    #     if newX < -self.dim or newX > self.dim:
    #         self.direction[0] *= -1
    #     else:
    #         self.position[0] = newX
    #     if newZ < -self.dim or newZ > self.dim:
    #         self.direction[2] *= -1
    #     else:
    #         self.position[2] = newZ

        # Se debe verificar que el objeto cubo, con su nueva posible direccion
        # no se salga del plano actual (DimBoard)
        # ...
    def setPosition(self, pos):
        self.position = pos

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glColor3f(*self.color)

        glBegin(GL_QUADS)

        # Definir un punto de referencia para el dibujado el cubo
        x, y, z = 0, 0, 0

        # Dimensiones de la caja
        width, height, depth = self.body

        # Cara frontal
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y, z)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + width, y, z)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + width, y + height, z)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y + height, z)

        # Cara trasera
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y, z + depth)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + width, y, z + depth)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + width, y + height, z + depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y + height, z + depth)

        # Cara izquierda
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y, z)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x, y, z + depth)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x, y + height, z + depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y + height, z)

        # Cara derecha
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x + width, y, z)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + width, y, z + depth)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + width, y + height, z + depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x + width, y + height, z)

        # Cara superior
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y + height, z)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + width, y + height, z)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + width, y + height, z + depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y + height, z + depth)

        # Cara inferior
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, y, z)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x + width, y, z)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x + width, y, z + depth)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y, z + depth)

        glEnd()
        glPopMatrix()