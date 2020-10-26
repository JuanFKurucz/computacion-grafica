import random

import pygame
from pygame.locals import *

from OpenGL.GL import *

from obj import Object

ang = 0.0
addVal = 0.0


def loadTexture(path):
    # Cargo la imagen a memoria. pygame se hace cargo de decodificarla correctamente
    surf = pygame.image.load(path)
    # Obtengo la matriz de colores de la imagen en forma de un array binario
    # Le indico el formato en que quiero almacenar los datos (RGBA) y que invierta la matriz, para poder usarla correctamente con OpenGL
    image = pygame.image.tostring(surf, "RGBA", 1)
    # Obentego las dimensiones de la imagen
    ix, iy = surf.get_rect().size
    # Creo una textura vacia en memoria de video, y me quedo con el identificador (texid) para poder referenciarla
    texid = glGenTextures(1)
    # Activo esta nueva textura para poder cargarle informacion
    glBindTexture(GL_TEXTURE_2D, texid)
    # Seteo los tipos de filtro a usar para agrandar y achivar la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # Cargo la matriz de colores dentro de la textura
    # Los parametros que le paso son:
    # - Tipo de textura, en este caso GL_TEXTURE_2D
    # - Nivel de mipmap, en este caso 0 porque no estoy usando mas niveles
    # - Formato en que quiero almacenar los datos en memoria de video, GL_RGB en este caso, porque no necesito canal Alfa
    # - Ancho de la textura
    # - Alto de la textura
    # - Grosor en pixels del borde, en este caso 0 porque no quiero agregar borde a al imagen
    # - Formato de los datos de la imagen, en este caso GL_RGBA que es como lo leimos con pygame.image
    # - Formato de los canales de color, GL_UNSIGNED_BYTE quiere decir que son 8bits para cada canal
    # - La imagen, en este caso la matriz de colores que creamos con pygame.image.tostring
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    # Una vez que tengo todo cargado, desactivo la textura para evitar que se dibuje por error mas adelante
    # Cada vez que quiera usarla, puedo hacer glBindTexture con el identificador (texid) que me guarde al crearla
    glBindTexture(GL_TEXTURE_2D, 0)
    # devuelvo el identificador de la textura para que pueda ser usada mas adelante
    return texid

luz = 0.2
def changeAng():
    global ang
    global addVal
    global luz
    ang += addVal
    luz+=addVal/1000


def init(ancho, largo):
    #Activo el manejo de texturas
    glEnable(GL_TEXTURE_2D)
    #Activo la textura 0 (hay 8 disponibles)
    glActiveTexture(GL_TEXTURE0)


    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1,0.1,0.1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glShadeModel(GL_SMOOTH)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,ancho,largo)
    glFrustum(-1,1,-1,1,1,1000)


    
def main():
    global ang
    global addVal
    pygame.init()
    cw = 800
    ch = 600
    display = (cw, ch)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    vel = 0.0
    box = Object.loadObj("./assets/knight_texturas.obj")
    text = loadTexture("./assets/knight.png")
    
    box.attachTexture(text)

    init(cw,ch)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glEnable(GL_LIGHTING)
                    addVal = -10
                elif event.key == pygame.K_RIGHT:
                    glDisable(GL_LIGHTING)
                    addVal = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    addVal = 0

        glLight(GL_LIGHT0, GL_AMBIENT, [luz, luz, luz, 1])
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -75)
        glRotatef(-90, 1, 0, 0)
        glRotatef(-45, 0, 0, 1)
        glRotatef(-22, 0, 1, 0)

        changeAng()
        glRotatef(ang, 0, 0, 1)
        
        box.draw()

        pygame.display.flip()

    glDeleteTextures([text])
    pygame.quit()
    quit()
main()
