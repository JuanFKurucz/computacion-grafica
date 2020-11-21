import json
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from model import Model
from objects.player import Player
from sound import Sound

from pygame import mixer

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


def load_sounds():
    assets_folder = "./assets/sounds/"
    sounds = {}
    with open("utils/config.json") as json_file:
        data = json.load(json_file)
        for sound_info in data["sounds"]:
            file = data["sounds"][sound_info]
            sounds[sound_info] = mixer.Sound(f"{assets_folder}{file}")
    Sound.sounds = sounds


def load_models(gouraud=None):
    models = {}
    with open("utils/config.json") as json_file:
        data = json.load(json_file)
        for model_info in data["models"]:
            instances = data["models"][model_info].get("instances")
            if not instances:
                instances = 1
            for i in range(instances):
                model_name = f"{model_info}_{i}" if instances > 1 else model_info
                position = data["models"][model_info].get("position", [0, 0, 0])
                new_position = []
                for p in position:
                    if p == "random":
                        new_position.append(random.randint(-10, 10))
                    else:
                        new_position.append(p)
                position = new_position

                sound_info = data["models"][model_info].get("default_sound")
                sound = None
                if sound_info:
                    sound = Sound(
                        sound_info.get("name"),
                        sound_info.get("volume", 1),
                        sound_info.get("loop", False),
                    )

                if model_info in ["knight", "weapon_k"]:
                    model = Player(
                        model_name,
                        data["models"][model_info]["assets"],
                        data["models"][model_info]["animations"],
                        data["models"][model_info]["texture"],
                        position,
                        data["models"][model_info].get("size"),
                        data["models"][model_info].get("speed", 1),
                        sound,
                    )
                else:
                    model = Model(
                        model_name,
                        data["models"][model_info]["assets"],
                        data["models"][model_info]["animations"],
                        data["models"][model_info]["texture"],
                        position,
                        data["models"][model_info].get("size"),
                        data["models"][model_info].get("speed", 1),
                        sound,
                    )
                model.load(data["models"][model_info]["default_animation"], gouraud=gouraud)
                models[model_name] = model
    return models
