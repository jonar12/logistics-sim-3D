from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Ambiente:
    def __init__(self, pos, scale, obj, angle, rotAxis, materiales=None, textures=None):
        self.scale = scale
        self.position = pos
        self.angle = angle
        self.textures = textures
        self.rotAxis = rotAxis
        self.materiales = materiales
        self.scene = obj
        self.display_list = self.create_display_list()
        
    def create_display_list(self):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)

        # Dibujar objetos para decorar el ambiente
        if self.textures is not None:
            self.render_with_textures()
        else:
            self.render_with_materials()
        glEndList()
        return display_list
        
    def render_with_materials(self):
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

        # Restablecer los colores a blanco
        glColor3f(1.0, 1.0, 1.0)


    def render_with_textures(self):
        glEnable(GL_TEXTURE_2D)
        for geometry in self.scene.geometry.values():
            material = geometry.visual.material
            if material.image is not None:
                # Usa el nombre del material como clave en lugar de material.image
                texture_key = material.name  # Asegúrate de que cada material tenga un nombre único
                if texture_key in self.textures:
                    texture_id = self.textures[texture_key]
                    glBindTexture(GL_TEXTURE_2D, texture_id)
            else:
                glBindTexture(GL_TEXTURE_2D, 0)

            vertices = geometry.vertices
            faces = geometry.faces
            tex_coords = geometry.visual.uv

            glBegin(GL_TRIANGLES)
            for face in faces:
                for i in range(3):
                    if tex_coords is not None:
                        glTexCoord2f(*tex_coords[face[i]])
                    glVertex3f(*vertices[face[i]])
            glEnd()
        glDisable(GL_TEXTURE_2D)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.angle, self.rotAxis[0], self.rotAxis[1], self.rotAxis[2])
        glScaled(self.scale[0], self.scale[1], self.scale[2])

        # Dibujar objetos para decorar el ambiente usando la lista de despliegue
        glCallList(self.display_list)
        glPopMatrix()

