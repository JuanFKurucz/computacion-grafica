from time import time

import pygame
from OpenGL.GL import *

from animation import Animation


class Model:
    def __init__(self, assets_folder, animations_prefix, texture_path):
        self.animations = {}
        self.current_animation = None
        self.texture_path = texture_path
        self.assets_folder = assets_folder
        self.animations_prefix = animations_prefix
        self.default_animation = None

    def add_animation(self, animation_type, animation):
        self.animations[animation_type] = animation

    def load_animations(self):
        for prefix in self.animations_prefix:
            animation = Animation(self.animations_prefix[prefix]["frames"])
            animation.load_animations(self.assets_folder, prefix)
            self.add_animation(prefix, animation)

    def load(self, default_animation):
        self.default_animation = default_animation
        self.load_animations()
        self.load_texture(f"{self.assets_folder}/{self.texture_path}")
        self.current_animation = self.animations[self.default_animation]

    def change_animation(self, animation_type=None):
        if not animation_type:
            animation_type = self.default_animation
        self.current_animation = self.animations[animation_type]
        self.current_animation.start_time = time()

    def draw(self, light=False):
        current_obj = self.current_animation.current_obj

        if current_obj.vertexes:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, current_obj.vertexes)

        if current_obj.normals:
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, current_obj.normals)

        if current_obj.textures:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glTexCoordPointer(2, GL_FLOAT, 0, current_obj.textures)
            glBindTexture(GL_TEXTURE_2D, self.texture)

        if light:
            # Si estoy usando shaders, le digo que la textura es la que esta activa en la posicion 0 (de las 8 disponibles)
            glUniform1i(self.texture, 0)

        glDrawArrays(GL_TRIANGLES, 0, len(current_obj.poligons))

        if current_obj.vertexes:
            glDisableClientState(GL_VERTEX_ARRAY)

        if current_obj.normals:
            glDisableClientState(GL_NORMAL_ARRAY)

        if current_obj.textures:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            glBindTexture(GL_TEXTURE_2D, 0)

    def load_texture(self, path):
        # Cargo la imagen a memoria. pygame se hace cargo de decodificarla correctamente
        surf = pygame.image.load(path)
        # Obtengo la matriz de colores de la imagen en forma de un array binario
        # Le indico el formato en que quiero almacenar los datos (RGBA) y que invierta la matriz, para poder usarla correctamente con OpenGL
        image = pygame.image.tostring(surf, "RGBA", 0)
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
        self.texture = texid
