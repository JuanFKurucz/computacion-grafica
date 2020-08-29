import pygame
from pygame.locals import *

from OpenGL.GL import *

def main():
        #estas instrucciones levantan una ventana grafica de pygame, con doble buffer y gestionadas por OpenGL
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        #Obtener la version de OpenGL soportada por mi driver de video.
        print(glGetString(GL_VERSION))

        #Comienzo a setear el pipeline para renderizar la escena
        #primero seteo las propiedades que no van a cambiar durante toda la ejecucion de mi aplicacion
        #es enste ejemplo sencillo van a ser las matrices de proyeccion y escala

        #activo el stack de matrices para la proyeccion
        glMatrixMode(GL_PROJECTION)
        
        #cargo una identidad para asegurarme que comience vacio
        glLoadIdentity()
        
        #glViewport crea la matriz de escala, que me permite transformar de unidades arbitrarias a pixels.
        #para esto necesita saber el tamano de la ventana en la que voy a dibujar
        glViewport(0,0,800,600)
        
        #glFrustum crea la matriz de Proyeccion.
        #recibe las dimensiones del plano de proyeccion (xmin,xmax,ymin,ymax), la distancia del foco al plano (znear = 1 en este ejemplo)
        #y el valor maximo de profundidad a partir del cual se descartan los puntos (zfar = 10000 en este ejemplo)
        glFrustum(-1,1,-1,1,1,10000)

        #estas variables las voy a usar para ir aumentando el angulo de rotacion del modelo
        ang = 0.0;
        vel = 0.0;

        #Esos vectores va a definir la gemometria a dibujar
        verts = [-1,0,0, 1,0,0, 0,1,0]
        colors= [ 1,0,0, 0,1,0, 0,0,1]
        indexs= [0,1,2]

        #Ahora comienzo un loop infinito (game loop), que seguira activo mientras la ventana de mi aplicacion este abierta
        while True:
                #Chequeo todos los eventos que sucedieron desde el cuadro anterior, utilizando la libreria de pygame
                for event in pygame.event.get():
                        #Si el evento es de tipo QUIT, significa que se quiere cerrar la ventana, y la aplicacion debe finalizar
                        if event.type == pygame.QUIT:
                                #Me aseguro de liberar todos los recursos reservados durante la ejecucion de pygame
                                #para luego poder terminar la aplicacion de forma segura
                                pygame.quit()
                                quit()
                        #Si el evento es una tecla presionada, chequeo cual es para reaccionar de forma acorde
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        vel = 1
                                elif event.key == pygame.K_RIGHT:
                                        vel = -1
                        #Si el evento es una tecla liberada, chequeo cual es para reaccionar de forma acorde
                        if event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                        vel = 0
                
                #Actualizo el estado de mi aplicacion, si vel es <> 0, entonces el angulo de rotacion va a variar
                ang += vel

                #Una vez que procesados los eventos y actualizado el estado de mi aplicacion (en este caso compuesto solo de la variable 'vel')
                #estoy en condiciones de empezar a dibujar el nuevo cuadro. Lo primero que debo hacer es limpiar el buffer de colores donde voy a dibujar.
                glClear(GL_COLOR_BUFFER_BIT)
                
                
                #Ahora puedo actualizar el estado de la maquina virtual para reflejar la escena que quiero dibujar

                #comienzo por setear la matriz modelo del objeto a dibujar
                #en este ejemplo es un unico objeto, pero en caso de ser varios esto se deberia hacer para cada uno

                #activo el stack de matrices MODELVIEW
                glMatrixMode(GL_MODELVIEW)
                #Limpio todas la transformaciones previas, seteando una identidad en el tope del stack
                glLoadIdentity()
                #ahora agrego las tranformaciones de mi modelo (por ahora camara no tenemos)
                #Roto el modelo sobre su centro en base al angulo acumulado en "ang"
                #y luego lo traslado frente a la camara, al moverlos a z=-2
                #notese que las transformaciones se aplican en el orden inverso al que se escriben en el codigo
                glTranslatef(0,0,-2)
                glRotatef(ang,0,1,0)

                #Una vez que todas las matrices del pipeline estan seteadas, puedo empezar a dibujar la geometria

                #Este codigo comentado corresponde al metodo directo, deprecado en versiones mas nuevas de OpenGL
                #Es una solucion poco eficiente y no se recomienda usarla
                # glBegin(GL_TRIANGLES)
                # glVertex3f(-1,0,0)
                # glVertex3f(1,0,0)
                # glVertex3f(0,1,0)
                # glEnd()

                #La forma recomendable de dibujar es usando Vertex Arrays
                #Primero le voy a indicar a la maquina de estados que arrays le voy a pasar, habilitandolos en la misma
                #habilito el array de vertices
                glEnableClientState(GL_VERTEX_ARRAY)
                #habilito el array de colores
                glEnableClientState(GL_COLOR_ARRAY)

                #Ahora le paso los vectores que almacenan los datos y sus caracteristicas
                #Paso un array de vertices, de 3 coordenadas en cada elemento, que son de tipo float. El paramaetro con valor 0 se llama "stride" y todavia no lo vamos a usar
                glVertexPointer(3, GL_FLOAT, 0, verts)

                #Paso un array de colores, de 3 coordenadas en cada elemento, que son de tipo float.
                glColorPointer(3, GL_FLOAT, 0, colors)

                #Ahora ya puedo dibujar. puedo mandar a dibujar los vertices como estan, o puedo usar el array de indices
                #para dibujar el array de vertices en el orden que estan declarados, uso glDrawArrays
                #indico que voy a dibujar triangulos, empezando en la posicion 0 del array, y voy a usar 3 vertices (cada vertice de 3 coordenadas)
                #glDrawArrays(GL_TRIANGLES, 0, 3)

                #para dibujar usando los indices, uso glDrawElements
                #indico que voy a dibujar triangulos, usando 3 indices de la lista, que los indices son de tipo unsigne int y la lista esta dada por la variable "indexs"
                glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, indexs)
                
                #una vez que termino de dibujar la escena, hago el flip de los buffers, para que se refresque la imagen en pantalla
                pygame.display.flip()

main()