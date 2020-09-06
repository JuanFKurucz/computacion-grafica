import random

import pygame
from pygame.locals import *

from OpenGL.GL import *
import numpy

main_colors = [
    1,1,1,
    1,0,0,
    1,1,0,
    0,1,1,
    0,0,1,
    0.5,0.5,0.5,
    0,0.5,0.5,
    0,0,0.5,
    0.5,0,0,
    0.5,0.5,0
]
index_color = -1

def return_color():
    global index_color
    index_color+=1
    return main_colors[index_color % len(main_colors)]

class Object:
    def __init__(self):
        self.name=""
        self.vertexes = []
        self.poligons = []
        self.colors = []

    def addVertex(self,x,y,z):
        self.vertexes.append(float(x))
        self.vertexes.append(float(y))
        self.vertexes.append(float(z))
    
    def addPoligon(self,x,y,z):
        self.poligons.append(int(x)-1)
        self.colors.append(return_color())
        self.poligons.append(int(y)-1)
        self.colors.append(return_color())
        self.poligons.append(int(z)-1)
        self.colors.append(return_color())


def loadObj(file):
    obj_file = open(file, 'r')
    lines = obj_file.readlines()
    
    obj = Object()

    for line in lines: 
        trimmed_line = line.strip()
        line_info = line.split(" ")
        if line.startswith("o"):
            obj.name=line_info[1]
        if line.startswith("v") or line.startswith("f"):
            try:
                x = line_info[1]
            except IndexError:
                x = 0
            try:
                y = line_info[2]
            except IndexError:
                y = 0
            try:
                z = line_info[3]
            except IndexError:
                z = 0
            if line.startswith("v"):
                obj.addVertex(x,y,z)
            else:
                obj.addPoligon(x,y,z)
    return obj
                


def main():
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

    ang = 0.0
    vel = 0.0
    box = loadObj("assets/box.obj")
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


        if change_cull_face:
            glEnable(GL_CULL_FACE)
        else:
            glDisable(GL_CULL_FACE)
        
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0,0,-2)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, box.vertexes)
        glColorPointer(3, GL_FLOAT, 0, box.colors)

        glDrawElements(GL_TRIANGLES, len(box.poligons), GL_UNSIGNED_INT, box.poligons)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        pygame.display.flip()


main()
