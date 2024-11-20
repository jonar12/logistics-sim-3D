import os # Ofrece funciones para interactuar con el sistema operativo
import requests # Permite enviar solicitudes HTTP 
from datetime import datetime
import asyncio
import aiohttp

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
from Caja import Caja

# Llamada a la API
URL_BASE = "http://localhost:8000"
response = requests.post(URL_BASE + "/simulations", allow_redirects = False)
data = response.json()
LOCATION = data["Location"] # ID de la simulación
print("Datos:", data)
print("Ubicación:", LOCATION)

# Obtener la dimensión del contenedor
print("Tamaño del contenedor:", data["container_corners"])
info_cajas = []

# Atributos de la caja
# [{'id': 2, 'pos': [15, 0, 20], 'is_stacked': True, 'WHD': [20, 20, 20], 'final_pos': [15, 0, 20]}, {'id': 1, 'pos': [15, 0, 0], 'is_stacked': True, 'WHD': [20, 50, 20], 'final_pos': [15, 0, 0]}]

# Realizar las llamadas a la API asíncronamente	
async def asynchronous_call():
    start_time = datetime.now()
    async with aiohttp.ClientSession() as session:
        for _ in range(100):
            async with session.get(URL_BASE + LOCATION) as response:
                response = await response.json()
                box = response["boxes"]
                print(box)
                info_cajas.append(box)
                
    end_time = datetime.now()
    print("Tiempo de ejecución:", end_time - start_time)

asyncio.run(asynchronous_call())


screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=1800.0
#Variables para definir la posicion del observador
EYE_X=300.0
EYE_Y=200.0
EYE_Z=300.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
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

# Arreglo para el manejo de los montacargas
montacargas = []
nMontacargas = 5

cajas = []

# Variables para el control del observador
theta = 0.0
radius = 300

# Arreglo para el manejo de texturas
textures = []
# filenames = ["./img1.bmp", "./wheel.jpeg", "./walle.jpeg", "./basura.bmp"]
filenames_objects = ["./textures/acero_negro.png", "./textures/llanta.png", "./textures/acero_amarillo.png", "./textures/caja.png", "./textures/piso_almacen.png"]

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
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
    
    for i in filenames_objects:
        Texturas(i)
    
    for i in range(nMontacargas):
        montacargas.append(Montacarga(DimBoard, 0.7, textures))
        
    for i in range(len(info_cajas[0])):
        cajas.append(Caja(DimBoard, 1, textures, 3, info_cajas[0][i]["pos"], info_cajas[0][i]["WHD"]))

def checkCollisions():
    for c in montacargas:
        for b in cajas:
            distance = sqrt(pow((b.position[0] - c.position[0]), 2) + pow((b.position[2] - c.position[2]), 2))
            if distance <= c.radiusCol:
                if c.status == 0 and b.alive:
                    b.alive = False
                    c.status = 1

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Se dibujan los montacargas   
    for obj in montacargas:
        obj.draw()
        # obj.update()    

    # Se dibuja el incinerador
    glColor3f(1.0, 0.5, 0.0)  # Color: Naranja
    square_size = 20.0  # Tamaño

    half_size = square_size / 2.0
    glBegin(GL_QUADS)
    glVertex3d(-half_size, 0.5, -half_size)
    glVertex3d(-half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, -half_size)
    glEnd()
    
    # Se dibujan las cajas
    for obj in cajas:
        obj.draw()
    
    # Se dibuja el piso del almacén
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

    checkCollisions()

# Cambio de la posición del observador
def handleMovement(keys):
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, theta
    
    if keys[pygame.K_w]:
        EYE_X -= cos(theta) + sin(theta) 
        EYE_Z -= sin(theta) + cos(theta)
        CENTER_X -= cos(theta) + sin(theta)
        CENTER_Z -= sin(theta) + cos(theta)

    if keys[pygame.K_s]:
        EYE_X += sin(theta) + cos(theta) 
        EYE_Z += cos(theta) + sin(theta)
        CENTER_X += sin(theta) + cos(theta)
        CENTER_Z += cos(theta) + sin(theta)

    if keys[pygame.K_a]:
        EYE_X -= cos(theta) - sin(theta)
        EYE_Z += sin(theta) + cos(theta)
        CENTER_X -= cos(theta) - sin(theta)
        CENTER_Z += sin(theta) + cos(theta)

    if keys[pygame.K_d]:
        EYE_X += cos(theta) - sin(theta)
        EYE_Z -= sin(theta) + cos(theta)
        CENTER_X += cos(theta) - sin(theta)
        CENTER_Z -= sin(theta) + cos(theta)

    # Movimiento vertical
    if keys[pygame.K_UP]:
        if EYE_Y < 500:
            EYE_Y += 1.0

    if keys[pygame.K_DOWN]:
        if EYE_Y > 0:
            EYE_Y -= 1.0

    # Rotación
    # if keys[pygame.K_LEFT]:
    #     theta += 1.0
    #     r = radians(theta)
    #     CENTER_X = EYE_X + cos(r)
    #     CENTER_Z = EYE_Z + sin(r)
    
    # if keys[pygame.K_RIGHT]:
    #     theta -= 1.0
    #     r = radians(theta)
    #     CENTER_X = EYE_X + cos(r)
    #     CENTER_Z = EYE_Z + sin(r)

Init()

done = False
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

    display()
    Axis()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()