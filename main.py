import pygame
from pygame.locals import *

from OpenGL.GL import *
import numpy

def main():
        pygame.init()
        cw = 800
        ch = 600
        display = (cw,ch)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        print glGetString(GL_VERSION)

        glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glViewport(0, 0, cw, ch)
	glFrustum(-1, 1, -1, 1, 1, 1000)

        angle = 0

        color = (255,128,60)
        plano = glGenLists(1)
        glNewList(plano, GL_COMPILE)
        glBegin(GL_TRIANGLES)
        glColor3ubv(color)
        glVertex3f(-1, 1, 0)
        glVertex3f( 1, 1, 0)
        glVertex3f(1, -1, 0)


        glColor3ub(255,0,255)
        glVertex3f(-1, -1, 0)
        glVertex3f( 1, -1, 0)
        glVertex3f(-1, 1, 0)
        glEnd()
        glEndList()

        verts = [-1,1,0,
                 1,1,0,
                 1,-1,0,
                 -1,-1,0,
                 1,-1,0,
                 -1,1,0]
        vertsList = [-1,1,0,
                     1,1,0,
                     1,-1,0,
                     -1,-1,0]
        verts = numpy.array(vertsList)

        indexs = [0,1,2,
                  3,2,0]

        colors = [255,0,0,
                  255,0,0,
                  255,0,0,
                  0,255,0,
                  0,255,0,
                  0,255,0]
        colors = numpy.array(colors)

        wire = False

        
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        quit()
                                elif event.key == pygame.K_m:
                                        if not wire:
                                                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                                        else:
                                                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                                        wire = not wire
                
                glMatrixMode(GL_MODELVIEW)
	        glLoadIdentity()

                glTranslatef(0,0,-2)
                glRotatef(angle, 0,1,0)
                glRotatef(angle, 1,0,0)
                glRotatef(angle, 0,0,1)
                glScalef(0.5,0.5,0.5)

                angle += 1

                glClear(GL_COLOR_BUFFER_BIT)

                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointer(3, GL_FLOAT, 0, verts)

                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, colors)

                #glDrawArrays(GL_TRIANGLES, 0, 6)
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, indexs)

                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)

                pygame.display.flip()
                

main()