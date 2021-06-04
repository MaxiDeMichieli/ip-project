from principal import *
from configuracion import *
from funcionesSeparador import *

import random
import math

def lectura(archivo, lista):
    for linea in archivo:
        lista.append(linea.replace("\n", "").replace("\r", ""))


def actualizar(silabasEnPantalla, posiciones, listaDeSilabas, totalTime, lastUpgrade):
    if totalTime > lastUpgrade:
        """ print(totalTime, lastUpgrade) """
        silaba = nuevaSilaba(listaDeSilabas)
        posicionX = randomNum(760)
        silabasEnPantalla.append(silaba)
        posiciones.append((posicionX, 0))

    newPositions = []
    """ print(posiciones) """
    for i in range(len(posiciones)):
        if posiciones[i][1] > 500:
            del silabasEnPantalla[i]
        else:
            newPositions.append((posiciones[i][0], posiciones[i][1]+1))
            """ print(newPositions) """
    del posiciones[:]
    posiciones.extend(newPositions)

def nuevaSilaba(silabas):
    randomNumber = int(randomNum(len(silabas)))
    return silabas[randomNumber]

def quitar(candidata, silabasEnPantalla, posiciones):
    silabasCandidatas = dameSilabas(candidata)
    """ print(silabasCandidatas) """
    for silaba in silabasCandidatas:
        if silaba in silabasEnPantalla:
            posicion = silabasEnPantalla.index(silaba)
            del silabasEnPantalla[posicion]
            del posiciones[posicion]
    """ print(silabasCandidatas) """


def dameSilabas(candidata):
    return separador(candidata).split('-')


def esValida(candidata, silabasEnPantalla, lemario):
    silabasCandidatas = dameSilabas(candidata)

    if candidata not in lemario:
        return False

    for silaba in silabasCandidatas:
        if silaba not in silabasEnPantalla:
            return False

    return True


def Puntos(candidata):
    total = 0

    for caracter in candidata:
        if caracter in VOCALES:
            """ print(caracter, '1') """
            total += 1
        elif caracter in DIFICILES:
            """ print(caracter, '5') """
            total += 5
        else:
            """ print(caracter, '2') """
            total += 2
    
    """ print(total) """
    return total

def procesar(candidata, silabasEnPantalla, posiciones, lemario):
    if esValida(candidata, silabasEnPantalla, lemario):
        quitar(candidata, silabasEnPantalla, posiciones)
        return Puntos(candidata)
    return 0

def randomNum(max):
    return random.random() * max