/* El color calculado en el vertex shader nos llega como entrada, ya interpolado para cada pixel */
varying vec4 vColor;
uniform sampler2D textura;
void main() {
    /*La unica salida de un fragment shader es el color que se va a pintar en ese pixel (gl_FragColor)
      En este caso, como la iluminacion ya la calcule en el vertex shader, me limito a pintsar con el color
      que me llega interpolado
    */
    gl_FragColor = vColor * texture2D(textura, gl_TexCoord[0].st);
}