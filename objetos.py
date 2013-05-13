import numpy as np
import Tkinter
from PIL import ImageDraw
import Image
import ImageTk
from sys import argv
import time
from math import fabs

def convolucion(imagen, h):
    iancho, ialtura = imagen.size
    imagen = imagen.convert('L')
    im = imagen.load()
    maltura, mancho = h.shape
    g = np.zeros(shape = (iancho, ialtura))

    for x in xrange(iancho):
        for y in xrange(ialtura):

            sum = 0.0
            c = 0.0001

            for i in xrange(mancho):
                zi = ( i - ( mancho / 2 )) 
                for j in xrange(maltura):
                    zj = ( j - ( maltura / 2 ) )

                    if x + zi >= 0 and x + zi < iancho and \
                            y + zj >= 0 and y + zj < ialtura:
                        sum += im[x + zi, y + zj] * h[i, j]
                        c += 1.0

            g[x, y] = sum / c

    return g

#metodo breath first search
#toma como parametro la matriz de la imagen, una copia de la matriz
#el color asignado RGB, la cola que es una lista, el ancho y la
#altura de la imagen original
def bfs(imagen, cola, ancho, altura, grupo):
    #toma el primer elemento de la cola y lo saca
    (x, y) = cola.pop(0)
    #si imagen no es color negro nos regresa un false
    if not imagen[x, y] == 0:
        return False
    #toma como blanco el pixel en la cola
    imagen[x, y] = 255 # ignora por poner en blanco
    grupo.append((x, y))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            (px, py) = (x + dx, y + dy)
            if px >= 0 and px < ancho and py >= 0 and py < altura:
                if imagen[px, py] == 0: # solo los negros entran en la cola
                    if (px, py) not in cola:
                        cola.append((px, py))
    return True

def asignColor(grupo):
    return ((grupo * 5 + 7) % 256, (grupo * 13 + 41) % 256, (grupo * 29 + 13) % 256)

#Metodo para hacer deteccion de objetos
#toma como parametro el nombre de la imagen
def deteccionObjetos(imagen):
    #Toma las proporciones de la imagen
    ancho, altura = imagen.size
    #toma es escala de grises la imagen
    imagen = imagen.convert('L')
    #carga la imagen para manipularla
    im = imagen.load()

    porAsignar = list()
    for x in xrange(ancho):
        for y in xrange(altura):
            if im[x, y] == 255: # blanco
                porAsignar.append((x, y))

    grupos = list()
    while True:
        grupo = list()
        # se coloca como false un marcador
        listo = False
        #Se recorre segun las proporciones
        for y in xrange(altura):
            for x in xrange(ancho):
                # si el pixel actual es negro
                #el marcador se coloca en true
                # y se sale del ciclo
                if im[x, y] == 0: # negro
                    listo = True
                    break
            if listo:
                break
        #si el marcador es falso sale del ciclo infinito
        if not listo:
            break
        #se crea la cola
        cola = list()
        # agrega la coordenada donde se encuentra nuestro pixel
        cola.append((x, y))
        #este ciclo seguira hasta que la cola no tenga nada
        while len(cola) > 0:
            #se hace breath first search
            #tomando como parametro matriz de la imagen, la matriz creada en rgb
            #la cola, el ancho y la altura de la imagen
            bfs(im, cola, ancho, altura, grupo)
        grupos.append(grupo)
        
    mayor = 0
    segundoMayor = 0
    fondoPos = None
    dronePos = None
    for pos in xrange(len(grupos)):
        tam = len(grupos[pos])
        if tam > mayor:
            fondoPos = pos
            mayor = tam
        elif tam > segundoMayor:
            dronePos = pos
            segundoMayor = tam

    fondo = grupos[fondoPos]
    drone = grupos[dronePos]
        
    for pos in xrange(len(grupos)):
        if pos != fondoPos and pos != dronePos:
            porAsignar += grupos[pos]

    total = ancho * altura

    ciclado = 0
    noSePudo = False
    while len(porAsignar) > 0:
        (x, y) = porAsignar.pop(0)
        buscando = True
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                vecino = (x + dx, y + dy) 
                if vecino in drone:
                    drone.append((x, y))
                    ciclado = 0
                    buscando = False
                    break
                if vecino in fondo:
                    fondo.append((x, y))
                    ciclado = 0
                    buscando = False
                    break
            if not buscando:
                break
        if buscando:
            porAsignar.append((x, y))
            ciclado += 1
            if ciclado > total / 50:
                noSePudo = True
                break

    if noSePudo:
        print 'No se pudo'

    clasificados = len(fondo) + len(drone)
    # total - clasificados debe ser cero

    cp = Image.new(mode = 'RGB', size = (ancho, altura))
    copia = cp.load()

    for (x, y) in fondo:
        copia[x, y] = 0, 255, 0

    minX = ancho
    maxX = 0
    minY = altura
    maxY = 0

    for (x, y) in drone:
        copia[x, y] = 0, 0, 255
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y

    print 'Esquina superior:',  minX, minY
    droneAncho = maxX - minX
    droneAltura = maxY - minY
    print 'Dimensiones:', droneAncho, droneAltura
    cx = minX + droneAncho / 2
    cy = minY + droneAltura / 2
    print 'Centro del drone:', cx, cy
    ix = ancho * 0.5
    iy = altura * 0.5

    print "Centro de la imagen x: ", ix, " y: ", iy
    dx = cx - ix
    dy = cy - iy
    print 'Diferencias:', dx, dy

    mx = ancho / 10
    print 'Tolerancia horizontal:', mx

    my = altura / 6
    print 'Tolerancia vertical:', my

    zmin = ancho / 3
    zmax = ancho / 2
    print 'Rango de profundidad:', zmin, zmax



    if droneAncho < zmin:
        print 'Acercarse'
    elif droneAncho > zmax:
        print 'Alejarse'
    elif fabs(dx) > mx: # se necesita correccion horizontal
        print 'Mover'
        if fabs(dx) > 2 * mx: # se necesita mucha correccion
            print 'mucho'
        if dx < 0:
            print 'a la derecha'
        else:
            print 'a la izquierda'
    elif fabs(dy) > my:
        print 'Mover hacia'
        if dy < 0:
            print 'abajo'
        else:
            print 'arriba'
    else:
        print 'Todo bien'

    for x in xrange(minX, maxX + 1):
        copia[x, minY] = 255, 0, 0

    for x in xrange(minX, maxX + 1):
        copia[x, maxY] = 255, 0, 0

    for y in xrange(minY, maxY + 1):
        copia[minX, y] = 255, 0, 0

    for y in xrange(minY, maxY + 1):
        copia[maxX, y] = 255, 0, 0

    for x in xrange(cx - 1, cx + 2):
        for y in xrange(cy - 1, cy + 2):
            copia[x, y] = 255, 255, 0

    return Image.fromarray(np.array(cp))


def main():
    imagen = Image.open(argv[1])
    original = imagen
    px = np.array([[-1,0,1], [-1,0,1], [-1,0,1]])
    py = np.array([[1,1,1], [0,0,0], [-1,-1,-1]])
    t1 = time.time()
    g = (convolucion(original, px)**2 + convolucion(original, py)**2) ** 0.5
    prom = np.average(g)
    ancho, altura = imagen.size
    imagen = imagen.convert('L')
    im = imagen.load()
    for x in xrange(ancho):
        for y in xrange(altura):
            if g[x, y] < 4 * prom / 3:
                im[x, y] = 0
            else:
                im[x, y] = 255

    resultado = deteccionObjetos(Image.fromarray(np.array(imagen)))
    
    root = Tkinter.Tk()
    tkimageOrig = ImageTk.PhotoImage(original)
    tkimageDeteccionObjetos = ImageTk.PhotoImage(resultado)

    Tkinter.Label(root, image = tkimageOrig).pack(side="right")
    Tkinter.Label(root, image = tkimageDeteccionObjetos).pack(side="left")
    t2 = time.time()
    print "Tiempo total: ", t2 - t1
    root.mainloop()

main()
