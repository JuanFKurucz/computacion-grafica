import json

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from model import Model
from objects.player import Player

# Uso esta funcion para compilar de forma individual el codigo de cada componente del shader (vertex y fragment)
# Le paso el path al archivo y el tipo de shader (GL_VERTEX_SHADER o GL_FRAGMENT_SHADER)
def compile_program(path, type):
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
def create_shader(vSource, fSource):
    # Creo y compilo el vertex shader
    vProgram = compile_program(vSource, GL_VERTEX_SHADER)
    # Creo y compilo el fragment shader
    fProgram = compile_program(fSource, GL_FRAGMENT_SHADER)
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


def load_models():
    models = {}
    with open("utils/config.json") as json_file:
        data = json.load(json_file)
        for model_info in data["models"]:
            if model_info == "knight":
                model = Player(
                    data["models"][model_info]["assets"],
                    data["models"][model_info]["animations"],
                    data["models"][model_info]["texture"],
                )
            else:
                model = Model(
                    data["models"][model_info]["assets"],
                    data["models"][model_info]["animations"],
                    data["models"][model_info]["texture"],
                )
            model.load(data["models"][model_info]["default_animation"])
            models[model_info] = model
    return models
