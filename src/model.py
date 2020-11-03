from time import time
from OpenGL.GL import *
from animation import Animation


class Model:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.texture = None

    def addAnimation(self, animation_type, animation):
        self.animations[animation_type] = animation

    def loadAnimations(self):
        idle = Animation(10)
        idle.loadAnimations("assets/knight", "knight_stand_")
        self.addAnimation("idle", idle)
        self.current_animation = self.animations["idle"]

    def changeAnimation(self, animation_type):
        self.current_animation = self.animations[animation_type]
        self.current_animation.start_time = time()

    def attachTexture(self, text):
        self.texture = text

    def draw(self, light=False):
        current_obj = self.current_animation.getCurrentObj()

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
