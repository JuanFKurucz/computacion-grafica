import json

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from model import Model

# Uso esta funcion para compilar de forma individual el codigo de cada componente del shader (vertex y fragment)
# Le paso el path al archivo y el tipo de shader (GL_VERTEX_SHADER o GL_FRAGMENT_SHADER)
def compileProgram(path, type):
    # Leo el codigo fuente desde el archivo
    sourceFile = open(path, "r")
    source = sourceFile.read()
    # Creo un shader vacio en memoria de video, del tipo indicado
    # En la variable shader queda almacenado un indice que nos va a permitir identificar este shader de ahora en mas
    shader = glCreateShader(type)
    # Le adjunto el codigo fuente leido desde el archivo
    glShaderSource(shader, source)
    # Intento compilarlo
    glCompileShader(shader)
    # Con la funcion glGelShaderiv puedo obtener el estado del compilador de shaders
    # En este caso le pido el stado de la ultima compilacion ejecutada
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        # Si la compilacion falla, muestro el error y retorno 0 (shader nulo)
        print(path + ": " + glGetShaderInfoLog(shader))
        # Me aseguro de liberar los recursos que reserve en memoria de vide, ya que no los voy a usar
        glDeleteShader(shader)
        return 0
    else:
        return shader


# Esta funcion me permite crear un programa de shading completo, basado en un vertex y un fragment shader
# Le paso el path a ambos codigos fuentes
def createShader(vSource, fSource):
    # Creo y compilo el vertex shader
    vProgram = compileProgram(vSource, GL_VERTEX_SHADER)
    # Creo y compilo el fragment shader
    fProgram = compileProgram(fSource, GL_FRAGMENT_SHADER)
    # Creo un programa de shading vacio en memoria de video
    shader = glCreateProgram()
    # Le adjunto el codigo objeto del vertex shader compilado
    glAttachShader(shader, vProgram)
    # Le adjunto el codigo objeto del fragment shader compilado
    glAttachShader(shader, fProgram)
    # Intento linkear el programa para generar un ejecutable en memoria de video
    glLinkProgram(shader)
    # Chequeo si la ejecucion del linkeo del programa fue exitosa
    if glGetProgramiv(shader, GL_LINK_STATUS) != GL_TRUE:
        # Si falla, imprimo el mensaje de error y libero los recursos
        print(glGetProgramInfoLog(shader))
        glDeleteProgram(shader)
        return 0
    # Una vez que el programa fue linkeado, haya sido exitoso o no, ya no necesito los shaders
    # individuales compilados, asi que libero sus recursos
    glDeleteShader(vProgram)
    glDeleteShader(fProgram)

    return shader


def loadModels():
    models = []
    with open("utils/config.json") as json_file:
        data = json.load(json_file)
        for model_info in data["models"]:
            model = Model(
                data["models"][model_info]["assets"],
                data["models"][model_info]["animations"],
                data["models"][model_info]["texture"],
            )
            model.load(data["models"][model_info]["default_animation"])
            models.append(model)
    return models


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    models = loadModels()

    # Creo un programa de shading y guardo la referencia en la variable gouraud
    gouraud = createShader("./assets/shaders/gouraud_vs.hlsl", "./assets/shaders/gouraud_fs.hlsl")

    # Activo el manejo de texturas
    glEnable(GL_TEXTURE_2D)
    # Activo la textura 0 (hay 8 disponibles)
    glActiveTexture(GL_TEXTURE0)
    # Llamo a la funcion que levanta la textura a memoria de video

    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [1, 1, 1, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1])
    glLight(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, display[0], display[1])
    glFrustum(-1, 1, -1, 1, 1, 1000)

    ang = 0.0
    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
    light = False
    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode(GL_FRONT_AND_BACK, mode)
                if event.key == pygame.K_z:
                    zBuffer = not zBuffer
                    if zBuffer:
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)
                if event.key == pygame.K_b:
                    bfc = not bfc
                    if bfc:
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)
                if event.key == pygame.K_c:
                    bfcCW = not bfcCW
                    if bfcCW:
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)
                if event.key == pygame.K_l:
                    light = not light
                    if light:
                        # Con la tecla L habilito y deshabilito el shader
                        glUseProgram(gouraud)
                    else:
                        glUseProgram(0)

                elif event.key == pygame.K_ESCAPE:
                    end = True

        mouse_movement = pygame.mouse.get_rel()
        ang += 0.5 * mouse_movement[0]

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, -20, -75)
        glRotatef(-45, 0, 1, 0)
        glRotatef(-90, 1, 0, 0)
        glRotatef(ang, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for model in models:
            model.draw()

        pygame.display.flip()

    # Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
    glDeleteProgram(gouraud)
    glDeleteTextures([model.texture for model in models])
    pygame.quit()
    quit()


main()
