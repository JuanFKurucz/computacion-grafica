# Computacion Grafica

## Manual de usuario

### Requisitos para correr el juego:

Bibliotecas de python:
- pygame 1.9.6
- PyOpenGL 3.1.5

Se recomienda crear un ambiente separado en python y correr `pip install -r requirements.txt` parado en la carpeta del proyecto para instalar estas bibliotecas

Para correr el juego pararse en la carpeta ROOT y ejecutar `python src\main.py`

### Controles

- Movimiento del personaje: se mueve con las teclas W, A, S, D. El personaje siempre se mueve en una dirección independientemente de la cámara.
- Movimiento de cámara: moviendo el mouse de izquierda a derecha por la pantalla del juego se podrá girar la cámara alrededor del personaje horizontalmente
- Adicionales:
  - Presionando espacio se hará la animación jump
  - Presionando CTRL izquierda se hará la animación crouch
  - Presionando F se hará la animación attack
  - Presionando 1 se hará la animación salute
  - Presionando 2 se hará la animación wave
  - Presionando 3 se hará la animación point

## Estructura y desarrollo

Se orientó al programa a seguir una modalidad OOP básica, donde tenemos el código separado en diferentes archivos, los cuales son:

- main.py
  - Se encarga del flujo principal del juego instanciando este y ejecutando el código en cada bucle
- obj.py
  - Se encarga de cargar archivos obj
- model.py
  - En base a los archivos obj se encarga de crear un modelo para poder dibujar y controlar estos fácilmente
- player.py
  - Sub clase de modelo para modelos que no son estáticos, requieren alguna acción por parte del jugador
- animation.py
  - Clase que es usada para almacenar objetos en model y cambiar entre ellos.
- sound.py
  - Clase que es usada para almacenar información de sonidos y su estado para ser reproducido
- utils.py
  - Funciones varias para cargado de configuraciones
- config.json
  - Este archivo contiene la configuracion del juego, en esta podemos ver los sonidos que se cargan, la configuracion de materiales y luces, y la configuracion de modelos asociadas a los sonidos.
