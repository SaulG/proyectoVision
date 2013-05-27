 ¿ De qué trata el proyecto ?

Primero daré una pequeña introducción al proyecto. Es un programa da ordenes a un drone para que se establesca dentro de la imagen de una camara, esto se puede realizar analizando la imagen tomada de la camara e identificando la posición del drone esto con el fin de identificar en que parte del area de la imagen se encuentra el drone y a partir de ahí decirle al drone que movimiento realizar para llegar al centro de la imagen la cual es nuestro caso ideal (estar en el centro de la imagen).

¿ Cuál es el propósito del proyecto ?

El propósito principal del proyecto es poder hacer un proyecto génerico para que se puedan realizar proyectos en donde el drone pueda realizar alguna cooperación con algún otro robot en la superficie, realizar alguna busqueda en la superficie ó seguir algún objetivo.


¿Cómo ejecutar el proyecto?

Actualmente se encuentra un archivo llamado detectaDrone.py el cual
este puede ser ejecutado de la siguiente manera:

                python detectaDrone.py

Este programa hará un conjunto de pruebas con varias imagenes tomadas
del drone en distintas posiciones que estas pueden ser acccedidas
dentro de la carpeta de SAMPLES, en dichas pruebas se evaluarán en que
dirección debería dirigirse el drone según el area detectada por
ciertas reglas establecidas.

¿Qué librerías se utilizaron?

   Las librerías utilizadas son las siguientes:

           PIL >= versión 1.1.7
           Tkinter >= versión 8.5
           Numpy >= versión 1.7.0

   Dichas librerías fueron usadas con Python versión 2.7.

Conclusiones de desempeño

El tamaño de la imagen procesada es de 320x129, su extensión es png y cada imagen tiene un peso promedio de 54 KB.

El procesador utilizado es de 2.3 GHz Intel Core i5.

Con una memoria RAM de 4GB.

Aunque el programa está diseñado para soportar cualquier tamaño de imagen, se utilizó en este caso un tamaño que puede ser mucho más reducido pero por motivos de demostración se tomaron de ese tamaño definido (320x 129).

El desempeño cambia mucho al momento de estar procesando una imagen en la que el drone es más grande que el fondo, como se puede ver en la gráfica con una imagen logró tardar ~25 segundos.



Trabajo a futuro

- Aplicación de velocidades del drone saber la velocidad de movimiento.

- Existe cierto problema al momento que el drone se encuentra parcialmente visto dentro de la imagen, ya que este lo detecta como si se estuviera alejando y pide que se acerque el drone (como podrán ver en la imagen de abajo).

