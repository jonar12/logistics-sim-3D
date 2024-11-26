import os # Ofrece funciones para interactuar con el sistema operativo
import requests # Permite enviar solicitudes HTTP 
from datetime import datetime
import asyncio
import aiohttp
import trimesh

import pywavefront
from process_mtl import *

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
from Contenedor import Contenedor
from Ambiente import Ambiente
from PIL import Image, ImageColor
from O_Wall import Walls

# Inicializar Pygame
pygame.init()

# Llamada a la API
URL_BASE = "http://localhost:8000"
response = requests.post(URL_BASE + "/simulations", allow_redirects = False)
data = response.json()
LOCATION = data["Location"] # ID de la simulación
sky = 2000

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
House2 = []
House3 = []
Car = []
objetos = []

# Realizar las llamadas a la API asíncronamente	
async def asynchronous_call():
    start_time = datetime.now()
    async with aiohttp.ClientSession() as session:
        for _ in range(1):
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
DimBoard = 240

# Arreglos para el manejo de los objetos
contenedor_class = []
montacargas_class = []
cajas_class = []
ambiente_class = []

# Variables para el control del observador
theta = -135.0
radius = 300

# Arreglo para el manejo de texturas
textures = []
filenames_objects = ["./textures/acero_negro.png", "./textures/llanta.png", "./textures/acero_amarillo.png", "./textures/caja.png", "./textures/piso_almacen.png"]

# Desde aqui es filename 5:
filenames_objects.append("./textures/sky.png")
filenames_objects.append("./textures/road.png")

# Cargamos los puntos del archivo .obj del Montacarga
montacarga_obj = pywavefront.Wavefront('./models_3D/Forklift.obj', create_materials=True, collect_faces=True)
montacarga_mtl = './models_3D/Forklift.mtl'

# Cargamos los archivos .obj para decorar el ambiente
truck_obj = pywavefront.Wavefront('./models_3D/truck.obj', create_materials=True, collect_faces=True)
truck_mtl = './models_3D/truck.mtl'

# Cargamos archivos .obj 
warehouse_obj = trimesh.load('./models_3D/warehouse.obj', force='scene')
redContainer = trimesh.load('./models_3D/redContainer.obj', force='scene')
box = trimesh.load('./models_3D/box.obj', force='scene')
platform = trimesh.load('./models_3D/platform.obj', force='scene')

# Cargar materiales del archivo .mtl
materiales = cargar_mtl(montacarga_mtl)
materiales2 = cargar_mtl(truck_mtl)

# Otros materiales y objetos
casa_1_obj = pywavefront.Wavefront('./models_3D/building/bulding.obj', create_materials=True, collect_faces=True)
casa_1_mtl = './models_3D/building/bulding.mtl'
casa_2_obj = pywavefront.Wavefront('./models_3D/building/building2.obj', create_materials=True, collect_faces=True)
casa_2_mtl = './models_3D/building/building2.mtl'

# Materiales y objetos
ob = []
ob.append(casa_1_obj)
ob.append(casa_2_obj)
mat = []
mat.append(cargar_mtl(casa_1_mtl))
mat.append(cargar_mtl(casa_2_mtl))

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

# Cargar cada textura del archivo .obj
def cargar_textura(image_source):
    img = image_source if isinstance(image_source, Image.Image) else Image.open(image_source)
    
    # Preparación de los datos de la textura
    img_data = img.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()
    width, height = img.size

    # Genera y configura la textura
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

# Cargar texturas de un archivo .obj que contiene imágenes
def cargar_objeto_con_texturas(scene):
    textures = {}
    for geometry in scene.geometry.values():
        material = geometry.visual.material
        if material.image is not None:
            # Se usa el nombre del material como clave   
            textures[material.name] = cargar_textura(material.image)
    return textures

def Init():
    
   # Pared frontal
    Wall.append([-40, -40, -40, DimBoard, False])
    Wall.append([-40, -40, DimBoard, -40, False])
    
    # Casa de prueba
    House.append([-150, 30, -90])
    House.append([-150, 10, 20])
    
    House.append([-50, 10, -110])
    
    House2.append([-40, -45, 45])
    House2.append([-30, 0, 150])
    House2.append([110, 0, -40])
    
    #House3.append([80, -1, 80])
    House3.append([90.0, 0, 80.0])
    
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
        objetos.append(Comp(DimBoard, 1, i,  ob[0], mat[0], [0.1,0.1,0.1], 45))
        
    for i in House2:   
        objetos.append(Comp(DimBoard, 1, i,  ob[1], mat[1], [10,10,10], 90))
            
    #w Texturas
    for i in filenames_objects:
        Texturas(i)

    # Cargar el objeto .obj de trimesh
    texturas = cargar_objeto_con_texturas(warehouse_obj)
    texturas2 = cargar_objeto_con_texturas(redContainer)
    texturas3 = cargar_objeto_con_texturas(box)
    texturas4 = cargar_objeto_con_texturas(platform)
    
    # Se crean los montacargas y las cajas por primera vez
    for i in range(len(montacargas[0])):
        montacargas_class.append(Montacarga(montacargas[0][i]["pos"], 180, montacarga_obj, materiales))
        
    for i in range(len(cajas[0])):
        cajas_class.append(Caja(cajas[0][i]["pos"], cajas[0][i]["final_pos"], cajas[0][i]["WHD"], cajas[0][i]["color"]))

    # Se crea el contenedor
    contenedor_class.append(Contenedor([width, height, depth], [0, 0, 0], container_color))

    # Crear el objetos para decorar el ambiente
    ambiente_class.append(Ambiente([7.3, 8.9, -7.0], [1.6, 3.0, 3.0], truck_obj, 90.0, [0.0, 1.0, 0.0], materiales=materiales2))

    ambiente_class.append(Ambiente([150.0, -8.9, 90.0], [3.5, 2.0, 2.0], warehouse_obj, -90.0, [0.0, 1.0, 0.0], textures=texturas))

    ambiente_class.append(Ambiente([135.0, -8.5, 185.0], [10.0, 10.0, 10.0], redContainer, -90.0, [0.0, 1.0, 0.0], textures=texturas2))

    ambiente_class.append(Ambiente([135.0, -8.5, 210.0], [10.0, 10.0, 10.0], redContainer, -90.0, [0.0, 1.0, 0.0], textures=texturas2))

    ambiente_class.append(Ambiente([135.0, 15.4, 197.5], [10.0, 10.0, 10.0], redContainer, -90.0, [0.0, 1.0, 0.0], textures=texturas2))

    ambiente_class.append(Ambiente([200.0, -8.5, 160.0], [0.1, 0.1, 0.1], box, -90.0, [0.0, 1.0, 0.0], textures=texturas3))

    ambiente_class.append(Ambiente([200.0, -8.5, 140.0], [0.1, 0.1, 0.1], box, -90.0, [0.0, 1.0, 0.0], textures=texturas3))

    ambiente_class.append(Ambiente([180.0, -8.5, 160.0], [0.07, 0.07, 0.07], box, -90.0, [0.0, 1.0, 0.0], textures=texturas3))

    ambiente_class.append(Ambiente([165.0, -8.5, 160.0], [0.07, 0.07, 0.07], box, -90.0, [0.0, 1.0, 0.0], textures=texturas3))

    ambiente_class.append(Ambiente([170.5, 2.0, 160.0], [0.07, 0.07, 0.07], box, -90.0, [0.0, 1.0, 0.0], textures=texturas3))

    ambiente_class.append(Ambiente([135.0, -6.2, 155.0], [13.0, 13.0, 13.0], platform, -90.0, [0.0, 1.0, 0.0], textures=texturas4))

    ambiente_class.append(Ambiente([133.0, -9.0, 152.0], [13.0, 13.0, 13.0], platform, 90.0, [0.0, 1.0, 0.0], textures=texturas4))

    ambiente_class.append(Ambiente([135.0, -4.0, 153.5], [13.0, 13.0, 13.0], platform, -90.0, [0.0, 1.0, 0.0], textures=texturas4))

    ambiente_class.append(Ambiente([126.5, -2.0, 153.5], [13.0, 13.0, 13.0], platform, 38.0, [0.0, 0.0, 1.0], textures=texturas4))

    ambiente_class.append(Ambiente([207, 1.7, 100.0], [13.0, 13.0, 13.0], platform, 70.0, [0.0, 0.0, 1.0], textures=texturas4))




def update_simulation(step):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar los ejes del sistema
    Axis()

    #Se dibuja el plano gris
    glColor3f(0.53, 0.81, 0.92)
    glBegin(GL_QUADS)
    glVertex3d(-sky, 300, -sky)
    glVertex3d(-sky, 300, sky)
    glVertex3d(sky, 300, sky)
    glVertex3d(sky, 300, -sky)
    glEnd()

    # Se actualizan los datos de los objetos

    # Actualizar la posición de los montacargas
    rotation_completed = True

    if step < len(montacargas) - 1:
        print("Step:", step)
        print("Montacarga:", montacargas[step])

        for cont, montacarga_data in enumerate(montacargas[step]):
            angle_rad = 0.0
            pos = montacarga_data["pos"]

            if step > 0:
                previous_pos = montacargas[step + 1][cont]["pos"]
                delta_x = pos[0] - previous_pos[0]
                delta_z = pos[2] - previous_pos[2]

                # Calcular el ángulo objetivo
                if delta_x < 0:
                    angle_rad = 90.0

                if delta_x > 0:
                    angle_rad = 270.0

                if delta_z < 0:
                    angle_rad = 0.0

                if delta_z > 0:
                    angle_rad = 180.0

                # Si el montacarga no está rotando, actualizar la posición y el ángulo objetivo
                if not montacargas_class[cont].isRotating():
                    montacargas_class[cont].setTargetAngle(angle_rad)
                    montacargas_class[cont].setPosition(pos)
                else:
                    rotation_completed = False

    # Actualizar la posición de las cajas solo si la rotación del montacarga ha terminado
    if rotation_completed and step < len(cajas):
        for cont, caja in enumerate(cajas[step]):
            pos = caja["pos"]
            cajas_class[cont].setPosition(pos)

    # Dibujar los montacargas
    for obj in montacargas_class:
        obj.update()
        obj.draw()
    
    # Se dibujan las cajas
    for obj in cajas_class:
        obj.returnToFinalPosition()
        obj.draw()

    # Se dibuja el contenedor
    for obj in contenedor_class:
        obj.draw()
    
    # Se dibuja las paredes
    for obj in Wall_Obj:
        obj.drawCube(textures, 5)
        
    # Dibujar los montacargas
    for obj in objetos:
       obj.draw()

    # Dibujar los objetos para decorar el ambiente
    for obj in ambiente_class:
        obj.draw()
    
    # Se dibuja el piso del almacén

    # Piso de concreto
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, -9.0, -DimBoard)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, -9.0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, -9.0, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, -9.0, -DimBoard)
    glEnd()

    # Carretera
    glBindTexture(GL_TEXTURE_2D, textures[6])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-10.5, -8.8, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-10.5, -8.8, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(33.0, -8.8, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(33.0, -8.8, 0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures[6])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-10.5, -8.8, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-10.5, -8.8, -DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(33.0, -8.8, -DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(33.0, -8.8, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    return rotation_completed

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
        # if EYE_Y > 0:
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

    rotation_completed = update_simulation(simulation_step)
    if rotation_completed:
        simulation_step += 1

    pygame.display.flip()
    pygame.time.wait(10)
    
pygame.quit()