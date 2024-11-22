from pygame.locals import *
from Cubo import Cubo

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

class Montacarga:
    def __init__(self, dim, vel, pos, obj, materiales):
        self.materiales = materiales
        self.dim = dim
        self.position = [pos[0], 0, pos[2]]
        # self.position = [pos[0], 18.5, pos[2]]
        # self.position = [pos[0], 0, pos[2]]
        
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]
        self.angle = 180
        self.vel = vel
        self.scene = obj
        self.platformHeight = -1.5
        self.platformUp = False
        self.platformDown = False
        self.radiusCol = 5
        self.status = 0
        self.trashID = -1
        self.display_list = self.create_display_list()

    def search(self):
        # Change direction to random
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]

    def targetCenter(self):
        # Set direction to center
        dirX = -self.position[0]
        dirZ = -self.position[2]
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]

    def setPosition(self, pos):
        self.position = [pos[0], 0, pos[2]]

    def update(self):
        if self.status == 1:
            delta = 0.01
            if self.platformHeight >= 0:
                self.targetCenter()
                self.status = 2
            else:
                self.platformHeight += delta
        elif self.status == 2:
            if (self.position[0] <= 10 and self.position[0] >= -10) and (self.position[2] <= 10 and self.position[2] >= -10):
                self.status = 3
            else:
                newX = self.position[0] + self.Direction[0] * self.vel
                newZ = self.position[2] + self.Direction[2] * self.vel
                if newX - 10 < -self.dim or newX + 10 > self.dim:
                    self.Direction[0] *= -1
                else:
                    self.position[0] = newX
                if newZ - 10 < -self.dim or newZ + 10 > self.dim:
                    self.Direction[2] *= -1
                else:
                    self.position[2] = newZ
                self.angle = math.acos(self.Direction[0]) * 180 / math.pi
                if self.Direction[2] > 0:
                    self.angle = 360 - self.angle
        elif self.status == 3:
            delta = 0.01
            if self.platformHeight <= -1.5:
                self.status = 4
            else:
                self.platformHeight -= delta
        elif self.status == 4:
            if (self.position[0] <= 20 and self.position[0] >= -20) and (self.position[2] <= 20 and self.position[2] >= -20):
                self.position[0] -= (self.Direction[0] * (self.vel/4))
                self.position[2] -= (self.Direction[2] * (self.vel/4))
            else:
                self.search()
                self.status = 0
        else:
            # Update position
            if random.randint(1,1000) == 69:
                self.search()
            newX = self.position[0] + self.Direction[0] * self.vel
            newZ = self.position[2] + self.Direction[2] * self.vel
            if newX - 10 < -self.dim or newX + 10 > self.dim:
                self.Direction[0] *= -1
            else:
                self.position[0] = newX
            if newZ - 10 < -self.dim or newZ + 10 > self.dim:
                self.Direction[2] *= -1
            else:
                self.position[2] = newZ
            self.angle = math.acos(self.Direction[0]) * 180 / math.pi
            if self.Direction[2] > 0:
                self.angle = 360 - self.angle

            # Move platform
            delta = 0.01
            if self.platformUp:
                if self.platformHeight >= 0:
                    self.platformUp = False
                else:
                    self.platformHeight += delta
            elif self.platformDown:
                if self.platformHeight <= -1.5:
                    self.platformUp = True
                else:
                    self.platformHeight -= delta

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

        # glPushMatrix()
        # glTranslatef(self.position[0], self.position[1], self.position[2])
        # glRotatef(self.angle, 0, 1, 0)
        # glScaled(5, 5, 5)
        # glColor3f(1.0, 1.0, 1.0)

        # Agregamos la texturas al cuerpo del Montacarga
        
        # # front face
        # glEnable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, self.textures[2])
        # glBegin(GL_QUADS)
        # glTexCoord2f(0.0, 0.0)
        # glVertex3d(1, 1, 1)
        # glTexCoord2f(0.0, 1.0)
        # glVertex3d(1, 1, -1)
        # glTexCoord2f(1.0, 1.0)
        # glVertex3d(1, -1, -1)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3d(1, -1, 1)

        # # 2nd face
        # glTexCoord2f(0.0, 0.0)
        # glVertex3d(-2, 1, 1)
        # glTexCoord2f(0.0, 1.0)
        # glVertex3d(1, 1, 1)
        # glTexCoord2f(1.0, 1.0)
        # glVertex3d(1, -1, 1)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3d(-2, -1, 1)

        # # 3rd face
        # glTexCoord2f(0.0, 0.0)
        # glVertex3d(-2, 1, -1)
        # glTexCoord2f(0.0, 1.0)
        # glVertex3d(-2, 1, 1)
        # glTexCoord2f(1.0, 1.0)
        # glVertex3d(-2, -1, 1)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3d(-2, -1, -1)

        # # 4th face
        # glTexCoord2f(0.0, 0.0)
        # glVertex3d(1, 1, -1)
        # glTexCoord2f(0.0, 1.0)
        # glVertex3d(-2, 1, -1)
        # glTexCoord2f(1.0, 1.0)
        # glVertex3d(-2, -1, -1)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3d(1, -1, -1)

        # # top
        # glTexCoord2f(0.0, 0.0)
        # glVertex3d(1, 1, 1)
        # glTexCoord2f(0.0, 1.0)
        # glVertex3d(-2, 1, 1)
        # glTexCoord2f(1.0, 1.0)
        # glVertex3d(-2, 1, -1)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3d(1, 1, -1)
        # glEnd()

        # # Head
        # glPushMatrix()
        # glTranslatef(0, 1.5, 0)
        # glScaled(0.8, 0.8, 0.8)
        # glColor3f(1.0, 1.0, 1.0)
        # head = Cubo(self.textures, 0)
        # head.draw()
        # glPopMatrix()
        # glDisable(GL_TEXTURE_2D)

        # # Wheels
        # glEnable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, self.textures[1])
        # glPushMatrix()
        # glTranslatef(-1.2, -1, 1)
        # glScaled(0.3, 0.3, 0.3)
        # glColor3f(1.0, 1.0, 1.0)
        # wheel = Cubo(self.textures, 0)
        # wheel.draw()
        # glPopMatrix()

        # glPushMatrix()
        # glTranslatef(0.5, -1, 1)
        # glScaled(0.3, 0.3, 0.3)
        # wheel = Cubo(self.textures, 0)
        # wheel.draw()
        # glPopMatrix()

        # glPushMatrix()
        # glTranslatef(0.5, -1, -1)
        # glScaled(0.3, 0.3, 0.3)
        # wheel = Cubo(self.textures, 0)
        # wheel.draw()
        # glPopMatrix()

        # glPushMatrix()
        # glTranslatef(-1.2, -1, -1)
        # glScaled(0.3, 0.3, 0.3)
        # wheel = Cubo(self.textures, 0)
        # wheel.draw()
        # glPopMatrix()
        # glDisable(GL_TEXTURE_2D)

        # Lifter
        # glPushMatrix()
        # if self.status == 1 or self.status == 2 or self.status == 3:
        #     self.drawTrash()
        # glColor3f(0.0, 0.0, 0.0)
        # glTranslatef(0, self.platformHeight, 0)  # Up and down
        # glBegin(GL_QUADS)
        # glTexCoord2f(0.0, 0.0)
        # glVertex3d(1, 1, 1)
        # glTexCoord2f(0.0, 1.0)
        # glVertex3d(1, 1, -1)
        # glTexCoord2f(1.0, 1.0)
        # glVertex3d(3, 1, -1)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3d(3, 1, 1)
        # glEnd()
        # glPopMatrix()
        # glPopMatrix()

    # def drawTrash(self):
    #     glPushMatrix()
    #     glTranslatef(2, (self.platformHeight + 1.5), 0)
    #     glScaled(0.5, 0.5, 0.5)
    #     glColor3f(1.0, 1.0, 1.0)

    #     glEnable(GL_TEXTURE_2D)
    #     glBindTexture(GL_TEXTURE_2D, self.textures[3])
    #     glBegin(GL_QUADS)

    #     # Front face
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3d(1, 1, 1)
    #     glTexCoord2f(1.0, 0.0)
    #     glVertex3d(-1, 1, 1)
    #     glTexCoord2f(1.0, 1.0)
    #     glVertex3d(-1, -1, 1)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3d(1, -1, 1)

    #     # Back face
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3d(-1, 1, -1)
    #     glTexCoord2f(1.0, 0.0)
    #     glVertex3d(1, 1, -1)
    #     glTexCoord2f(1.0, 1.0)
    #     glVertex3d(1, -1, -1)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3d(-1, -1, -1)

    #     # Left face
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3d(-1, 1, 1)
    #     glTexCoord2f(1.0, 0.0)
    #     glVertex3d(-1, 1, -1)
    #     glTexCoord2f(1.0, 1.0)
    #     glVertex3d(-1, -1, -1)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3d(-1, -1, 1)

    #     # Right face
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3d(1, 1, -1)
    #     glTexCoord2f(1.0, 0.0)
    #     glVertex3d(1, 1, 1)
    #     glTexCoord2f(1.0, 1.0)
    #     glVertex3d(1, -1, 1)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3d(1, -1, -1)

    #     # Top face
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3d(-1, 1, 1)
    #     glTexCoord2f(1.0, 0.0)
    #     glVertex3d(1, 1, 1)
    #     glTexCoord2f(1.0, 1.0)
    #     glVertex3d(1, 1, -1)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3d(-1, 1, -1)

    #     # Bottom face
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3d(-1, -1, 1)
    #     glTexCoord2f(1.0, 0.0)
    #     glVertex3d(1, -1, 1)
    #     glTexCoord2f(1.0, 1.0)
    #     glVertex3d(1, -1, -1)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3d(-1, -1, -1)

    #     glEnd()
    #     glDisable(GL_TEXTURE_2D)

    #     glPopMatrix()