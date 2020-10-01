import random

import pygame
from pygame.locals import *

from OpenGL.GL import *

from obj import Object

ang = 0.0
addVal = 0.0


def changeAng():
    global ang
    global addVal
    ang += addVal


def main():
    global ang
    global addVal
    pygame.init()
    cw = 800
    ch = 600
    display = (cw, ch)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    print(glGetString(GL_VERSION))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, cw, ch)
    glFrustum(-1, 1, -1, 1, 1, 1000)

    vel = 0.0
    box = Object.loadObj("../assets/knight.obj")
    change_wire_mode = False
    change_cull_face = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if change_wire_mode:
                        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                    else:
                        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                    change_wire_mode = not change_wire_mode
                elif event.key == pygame.K_c:
                    change_cull_face = not change_cull_face
                elif event.key == pygame.K_LEFT:
                    addVal = -10
                elif event.key == pygame.K_RIGHT:
                    addVal = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    addVal = 0

        if change_cull_face:
            glEnable(GL_CULL_FACE)
        else:
            glDisable(GL_CULL_FACE)
        changeAng()

        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -75)
        glRotatef(-90, 1, 0, 0)
        glRotatef(ang, 0, 0, 1)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, box.vertexes)
        glColorPointer(3, GL_FLOAT, 0, box.colors)

        glDrawElements(GL_TRIANGLES, len(box.poligons), GL_UNSIGNED_INT, box.poligons)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        pygame.display.flip()


main()
