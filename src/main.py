import pygame
from pygame.locals import *

from OpenGL.GL import *

from utils import load_models, create_shader


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    models = load_models()

    # Creo un programa de shading y guardo la referencia en la variable gouraud
    gouraud = create_shader("./assets/shaders/gouraud_vs.hlsl", "./assets/shaders/gouraud_fs.hlsl")

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

    models["knight"].rotation = -200
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    models["knight"].add_move("front")
                if event.key == pygame.K_s:
                    models["knight"].add_move("back")
                if event.key == pygame.K_a:
                    models["knight"].add_move("left")
                if event.key == pygame.K_d:
                    models["knight"].add_move("right")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    models["knight"].remove_move("front")
                if event.key == pygame.K_s:
                    models["knight"].remove_move("back")
                if event.key == pygame.K_a:
                    models["knight"].remove_move("left")
                if event.key == pygame.K_d:
                    models["knight"].remove_move("right")

                if event.key == pygame.K_SPACE:
                    models["knight"].jump()
                if event.key == pygame.K_LCTRL:
                    models["knight"].crouch()

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
        ang %= 360

        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for model in models:
            movements = models["knight"].movement
            if model != "knight":
                front = 0
                left = 0
                if "front" in movements:
                    front = 1
                elif "back" in movements:
                    front = -1
                if "right" in movements:
                    left = -1
                elif "left" in movements:
                    left = 1

                if front < 0 and left < 0:
                    models["knight"].rotation = 45
                elif front < 0 and left > 0:
                    models["knight"].rotation = -45
                elif front > 0 and left < 0:
                    models["knight"].rotation = -225
                elif front > 0 and left > 0:
                    models["knight"].rotation = -135
                elif front < 0:
                    models["knight"].rotation = 0
                elif front > 0:
                    models["knight"].rotation = -180
                elif left < 0:
                    models["knight"].rotation = -270
                elif left > 0:
                    models["knight"].rotation = -90
                models[model].x += front
                models[model].y += left
            models[model].draw(angle=ang)

        pygame.display.flip()

    # Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
    glDeleteProgram(gouraud)
    glDeleteTextures([models[model].texture for model in models])
    pygame.quit()
    quit()


main()
