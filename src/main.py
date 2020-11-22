import pygame
from pygame.locals import *

from OpenGL.GL import *

from utils import load_lighting, load_materials, load_models, load_sounds


def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.mixer.init()
    pygame.mouse.set_visible(False)  # Esconder cursor del mouse

    # Activo el manejo de texturas
    glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)

    load_materials()
    load_lighting()

    glShadeModel(GL_SMOOTH)  # shaders
    glEnable(GL_DEPTH_TEST)  # z-buffer
    glEnable(GL_CULL_FACE)  # backface culling
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, display[0], display[1])
    glFrustum(-1, 1, -1, 1, 1, 1000)


def main():
    init()

    load_sounds()
    models = load_models()

    ang = 0.0
    end = False

    if "weapon_k" in models:
        models["knight"].attach_model(models["weapon_k"])
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
                    models["knight"].do_action("jump")
                if event.key == pygame.K_LCTRL:
                    models["knight"].do_action("crouch")
                if event.key == pygame.K_f:
                    models["knight"].do_action("attack")
                if event.key == pygame.K_h:
                    models["knight"].do_action("salute")
                if event.key == pygame.K_c:
                    models["knight"].do_action("wave")
                if event.key == pygame.K_p:
                    models["knight"].do_action("point")

                elif event.key == pygame.K_ESCAPE:
                    end = True

        # Giro el angulo segun el movimiento del mouse
        mouse_movement = pygame.mouse.get_rel()
        ang += 0.5 * mouse_movement[0]
        ang %= 360

        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        player_models = models["knight"].get_models()
        movements = models["knight"].get_movement()

        # Chequeo de movimiento actual
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

        # Rotacion de modelos asociados al personaje
        for player_model in player_models:
            if front < 0 and left < 0:
                models[player_model].rotation = 45
            elif front < 0 and left > 0:
                models[player_model].rotation = -45
            elif front > 0 and left < 0:
                models[player_model].rotation = -225
            elif front > 0 and left > 0:
                models[player_model].rotation = -135
            elif front < 0:
                models[player_model].rotation = 0
            elif front > 0:
                models[player_model].rotation = -180
            elif left < 0:
                models[player_model].rotation = -270
            elif left > 0:
                models[player_model].rotation = -90

        # Dibujo de modelos
        for model in models:
            # Movimiento de ambiente (todo menos modelos asociados al personaje)
            if model not in player_models:
                models[model].move_x(front)
                models[model].move_y(left)

            models[model].draw(angle=ang)

            # Reproduccion de audio
            if models[model].current_sound:
                current_sound = models[model].current_sound.play()

        pygame.display.flip()

    # Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
    glDeleteTextures([models[model].texture for model in models])
    pygame.quit()
    quit()


main()
