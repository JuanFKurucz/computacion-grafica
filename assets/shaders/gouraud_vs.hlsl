/*Defino un color como salida del shader, para que llegue interpolado al fragment shader*/
varying vec4 vColor;

/*Voy a implementar Gourad Shadig, calculando la ecuacion de Lambert para cada vertice
  e interpolando el color resultante.
*/
void main() {
    /* Multiplico el vertice de entrada, en Object space, por la matriz modelview, llevandolo a Camera Space*/
    vec4 V = gl_ModelViewMatrix * gl_Vertex;
    /* El vector de la luz es el que va desde el vertice hasta la fuente de luz */
    vec3 L = gl_LightSource[0].position.xyz - V.xyz;
    /* La normal tambien debe estar en camera space, por lo que debe ser multiplicada por la model view
       Como la normal es un vector (no un punto, como los vertices), no es correcto aplicarle traslaciones
       por eso en lugar de la modelview uso la matriz NormalMatrix, que tiene las mismas transformaciones 
       pero sin traslaciones
    */
    vec3 N = gl_NormalMatrix * gl_Normal;
    /* Aplico la ecuacion de Lambert, solo la parte difusa en este caso */
    vColor = gl_FrontLightProduct[0].ambient + gl_FrontLightProduct[0].diffuse * max(0,dot(N,L));
    /* Por ultimo, todo Vertex shader requiere que la variable gl_Position siempre sea cargada, porque 
       corrsponde al vertice proyectado que se usara como entrada del attribute mapping.
       Por eso tomamos el vertice en Camera Space y lo multiplicamos por la matriz de proyeccion
    */
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = gl_ProjectionMatrix * V;
}