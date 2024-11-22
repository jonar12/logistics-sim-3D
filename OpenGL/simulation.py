import os # Ofrece funciones para interactuar con el sistema operativo
import requests # Permite enviar solicitudes HTTP 
from datetime import datetime
import asyncio
import aiohttp

import pywavefront
from process_mtl import cargar_mtl

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Cambiamos el directorio de trabajo
# os.chdir(os.path.join(os.getcwd(), "OpenGL")) # chdir: Se utiliza para cambiar el directorio de trabajo actual a la ruta especificada

from math import *
from random import *
from Montacarga import Montacarga
from Fake_Compiler import Comp
from Caja import Caja
from Camion import Camion
from PIL import ImageColor
from O_Wall import Walls

# Llamada a la API
URL_BASE = "http://localhost:8000"
response = requests.post(URL_BASE + "/simulations", allow_redirects = False)
data = response.json()
LOCATION = data["Location"] # ID de la simulación

# Obtener la dimensión del contenedor
(xColor, yColor, zColor) = ImageColor.getcolor("#e4ff00", "RGB")
container_color = (xColor / 255, yColor / 255, zColor / 255)

# Obtener los datos del contenedor
container = data["container"]

# Obtener las dimensiones del contenedor
depth = container["depth"]
height = container["height"]
width = container["width"]

# Guardar los datos de las cajas y los montacargas
cajas = []
montacargas = []

# Almaceniamiento de diversos objetos:
Wall = []
Wall_Obj = []
House = []
objetos = []

# Realizar las llamadas a la API asíncronamente	
async def asynchronous_call():
    start_time = datetime.now()
    async with aiohttp.ClientSession() as session:
        for _ in range(400):
            async with session.get(URL_BASE + LOCATION) as response:
                response = await response.json()

                # Agregamos la información de los montacargas
                montacarga = response["lifts"]

                # Agregamos la información de las cajas
                caja = response["boxes"]

                # Procesamos los colores de las cajas
                for i in range(len(caja)):
                    color = caja[i]["color"]
                    x, y, z = ImageColor.getcolor(color, "RGB")
                    caja[i]["color"] = (x / 255, y / 255, z / 255)

                montacargas.append(montacarga)
                cajas.append(caja)

    end_time = datetime.now()
    print("Tiempo de ejecución:", end_time - start_time)

asyncio.run(asynchronous_call())
print("Caja:", cajas[0])
# Definimos las dimensiones de la pantalla
screen_width = 500
screen_height = 500

#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=1800.0
#Variables para definir la posicion del observador
EYE_X=300.0
EYE_Y=100.0
EYE_Z=300.0
CENTER_X=0.0
CENTER_Y=0.0
CENTER_Z=0.0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

# Dimension del plano
DimBoard = 200

# Arreglos para el manejo de los objetos
contenedor_class = []
montacargas_class = []
cajas_class = []

# Variables para el control del observador
theta = -135.0
radius = 300

# Arreglo para el manejo de texturas
textures = []
filenames_objects = ["./textures/acero_negro.png", "./textures/llanta.png", "./textures/acero_amarillo.png", "./textures/caja.png", "./textures/piso_almacen.png"]

# Desde aqui es filename 5:
filenames_objects.append("./textures/sky.png")

# Cargamos los puntos del archivo .obj del Montacarga
montacarga_obj = pywavefront.Wavefront('./models_3D/Forklift.obj', create_materials=True, collect_faces=True)
montacarga_mtl = './models_3D/Forklift.mtl'

# Cargar materiales del archivo .mtl
materiales = cargar_mtl(montacarga_mtl)



# Otros materiales y objetos
casa_1_obj = pywavefront.Wavefront('./models_3D/houses/obj_House.obj', create_materials=True, collect_faces=True)
casa_1_mtl = './models_3D/houses/material.lib'

# Materiales y objetos
ob = []
ob.append(casa_1_obj)
mat = []
mat.append(cargar_mtl(casa_1_mtl))

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

def Init():
    
    # Pared frontal
    Wall.append([-40, -40, -40, DimBoard, False])
    Wall.append([-40, -40, DimBoard, -40, False])
    
    # Casa de prueba
    House.append([-40, 0, 0])
    
    House.append([-40, 0, 150])
    
    #CREACION DE LOS OBJETOS INDICADOS
    for i in Wall:
        [x11, z11, x22, z22, jump] = i
        Wall_Obj.append(Walls(x11, z11, x22, z22, jump))
    
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Simulacion de almacen")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    #Creando a las casas
    for i in House:   
        objetos.append(Comp(DimBoard, 1, i,  ob[0], mat[0], [10,10,10]))
    
    # Texturas
    for i in filenames_objects:
        Texturas(i)
    
    # Se crean los montacargas y las cajas por primera vez
    for i in range(len(montacargas[0])):
        montacargas_class.append(Montacarga(DimBoard, 0.7, montacargas[0][i]["pos"], montacarga_obj, materiales))
        
        
    for i in range(len(cajas[0])):
        cajas_class.append(Caja(DimBoard, 1, textures, 3, cajas[0][i]["pos"], cajas[0][i]["WHD"], cajas[0][i]["color"]))

    # Se crea el contenedor
    contenedor_class.append(Camion([depth, height, width], [0, 0, 0], container_color))

def display(step):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Se actualizan los datos de los objetos

    # Actualizar la posición de los montacargas
    if step < len(montacargas):
        for cont, montacarga in enumerate(montacargas[step]):
            pos = montacarga["pos"]
            montacargas_class[cont].setPosition(pos)

    # Actualizar la posición de las cajas
    if step < len(cajas):
        for cont, caja in enumerate(cajas[step]):
            pos = caja["pos"]
            cajas_class[cont].setPosition(pos)

    # Dibujar los montacargas
    for obj in montacargas_class:
        obj.draw()
    
    # Se dibujan las cajas
    for obj in cajas_class:
        obj.draw()

    # Se dibuja el contenedor
    for obj in contenedor_class:
        obj.draw()
    
    # Se dibuja las paredes
    for obj in Wall_Obj:
        obj.drawCube(textures, 5) # 0 sky 1 void
        
    # Dibujar los montacargas
    for obj in objetos:
        obj.draw()
    
    # Se dibuja el piso del almacén
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0, -DimBoard)

    glEnd()
    glDisable(GL_TEXTURE_2D)

# Manipulación de la posición del observador
speed_movement = 1.0
def handleMovement(keys):
    global EYE_X, EYE_Y, EYE_Z
    global CENTER_X, CENTER_Y, CENTER_Z
    global theta

    # Calcular el vector de dirección a partir de theta
    r = radians(theta)
    dir_x = cos(r)
    dir_z = sin(r)

    # Movimiento hacia adelante y hacia atrás (W y S)
    if keys[pygame.K_w]:
        EYE_X += dir_x * speed_movement
        EYE_Z += dir_z * speed_movement
    if keys[pygame.K_s]:
        EYE_X -= dir_x * speed_movement
        EYE_Z -= dir_z * speed_movement

    # Movimiento lateral (A y D)
    if keys[pygame.K_a]:
        EYE_X += dir_z * speed_movement
        EYE_Z -= dir_x * speed_movement

    if keys[pygame.K_d]:
        EYE_X -= dir_z * speed_movement
        EYE_Z += dir_x * speed_movement
        

    # Movimiento vertical (Flechas arriba y abajo)
    if keys[pygame.K_UP]:
        if EYE_Y < 500:
            EYE_Y += speed_movement

    if keys[pygame.K_DOWN]:
        if EYE_Y > 0:
            EYE_Y -= speed_movement

    # Rotación izquierda y derecha (Flechas izquierda y derecha)
    if keys[pygame.K_LEFT]:
        theta -= speed_movement  # Rotar a la izquierda
    if keys[pygame.K_RIGHT]:
        theta += speed_movement  # Rotar a la derecha

    # Mantener theta en el rango [0, 360)
    theta %= 360

    # Actualizar el punto de vista (CENTER_X, CENTER_Y, CENTER_Z)
    r = radians(theta)
    dir_x = cos(r)
    dir_z = sin(r)

    CENTER_X = EYE_X + dir_x
    CENTER_Y = EYE_Y  # Mantener la misma altura
    CENTER_Z = EYE_Z + dir_z
    # CENTER_X = 0.0
    # CENTER_Y = 0.0
    # CENTER_Z = 0.0
    
Init()

done = False

# Pasos de simulación
simulation_step = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()  # Checking pressed keys

    # Movimientos del observador
    handleMovement(keys)

    glLoadIdentity() # Cargamos la matriz identidad para limpiar la matriz de modelado
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    # Actualizar objetos por cada segundo
    display(simulation_step)
    simulation_step += 1
    Axis()

    pygame.display.flip()
    pygame.time.wait(10)
    
pygame.quit()