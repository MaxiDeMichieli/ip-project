from principal import *
from configuracion import *
from funcionesSeparador import *
import json
from datetime import datetime

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

def moverMenu(opciones, seleccionada, accion):
    if seleccionada == 0 and accion == -1:
        return len(opciones) - 1
    elif seleccionada == len(opciones) - 1 and accion == 1:
        return 0
    else:
        return seleccionada + accion

def dibujarInicio(screen, opciones, opcionSeleccionada, jugador):
    defaultFont= pygame.font.Font( pygame.font.get_default_font(), 40)
    smallFont= pygame.font.Font( pygame.font.get_default_font(), 20)
    yInicial = 150

    screen.blit(smallFont.render("Jugador: " + jugador, 1, COLOR_TEXTO), (50, 50))

    for i in range(len(opciones)):
        posicion = (200, yInicial)

        if opciones[i] == opcionSeleccionada:
            screen.blit(defaultFont.render(opciones[i] + "*", 1, COLOR_LETRAS), posicion)
        else:
            screen.blit(defaultFont.render(opciones[i], 1, COLOR_TEXTO), posicion)

        yInicial += 100

def dibujarPuntajeJuego(screen, puntos):
    defaultFont= pygame.font.Font( pygame.font.get_default_font(), 40)

    screen.blit(defaultFont.render("PUNTAJE FINAL", 1, COLOR_TEXTO), (200, 150))
    screen.blit(defaultFont.render(str(puntos), 1, COLOR_LETRAS), (200, 250))

def dibujarIngresaNombre(screen, jugador):
    defaultFont= pygame.font.Font( pygame.font.get_default_font(), 40)
    smallFont= pygame.font.Font( pygame.font.get_default_font(), 20)

    screen.blit(defaultFont.render("INGRESA TU NOMBRE", 1, COLOR_TEXTO), (200, 150))
    screen.blit(defaultFont.render(jugador, 1, COLOR_LETRAS), (200, 250))
    screen.blit(smallFont.render("Presiona enter para continuar", 1, COLOR_TEXTO), (200, 450))

def procesarUsuario(jugador):
    if jugador == "":
        return

    fileR = open("users.json", "r")
    data = json.load(fileR)

    if not jugador in data:
        data[jugador] = []

        fileW = open("users.json", "w")
        json.dump(data, fileW, indent=2)
        fileW.close()

    fileR.close()

def guardarPuntaje(jugador, puntos):
    fileR = open("users.json", "r")
    data = json.load(fileR)
    
    nuevoPuntaje = {}
    nuevoPuntaje['score'] = puntos
    nuevoPuntaje['date'] = datetime.now().strftime("%d/%m/%Y")

    data[jugador].append(nuevoPuntaje)

    fileW = open("users.json", "w")
    json.dump(data, fileW, indent=2)

    fileW.close()
    fileR.close()

def buscarMejoresPuntajes(jugador):
    fileR = open("users.json", "r")
    data = json.load(fileR)

    return sorted(data[jugador], key=lambda x: x['score'], reverse=True)
    fileR.close()

def dibujarPuntajes(screen, jugador, puntajes):
    defaultFont= pygame.font.Font( pygame.font.get_default_font(), 40)
    smallFont= pygame.font.Font( pygame.font.get_default_font(), 20)
    yInicial = 180

    screen.blit(smallFont.render("Jugador: " + jugador, 1, COLOR_TEXTO), (50, 50))
    screen.blit(smallFont.render("VOLVER*", 1, COLOR_LETRAS), (600, 50))

    if len(puntajes) == 0:
        screen.blit(defaultFont.render("No tienes puntajes", 1, COLOR_TEXTO), (200, 150))
    else:
        screen.blit(defaultFont.render("Mejores puntajes", 1, COLOR_TEXTO), (200, 100))

    for puntaje in puntajes[:10]:
        score = str(puntaje['score'])
        fecha = str(puntaje['date'])
        screen.blit(smallFont.render(score+"  -  "+fecha , 1, COLOR_TEXTO), (200, yInicial))
        yInicial += 40
