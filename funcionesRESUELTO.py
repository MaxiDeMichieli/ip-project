from principal import *
from configuracion import *
from funcionesSeparador import *
import json
from datetime import datetime

import random
import math

def lectura(archivo, lista):
    for linea in archivo: # recorre cada linea del archivo
        lista.append(linea.replace("\n", "").replace("\r", "")) # agrega a la lista cada linea del archivo


def actualizar(silabasEnPantalla, posiciones, listaDeSilabas):
    if not len(posiciones) or posiciones[len(posiciones) - 1][1] > 40: # si aun no hay posiciones o la ultima posicion ya esta a mas de 40px en el eje y
        silaba = nuevaSilaba(listaDeSilabas)
        posicionX = randomNum(ANCHO - 40)
        silabasEnPantalla.append(silaba) # agrega la nueva silaba a las silabas en pantalla
        posiciones.append((posicionX, 0)) # agrega la nueva posicion a la lista de posiciones

    newPositions = []
    for i in range(len(posiciones)):
        if posiciones[i][1] > 500: # si la posiciones en el eje y super los 500px...
            del silabasEnPantalla[i] # elimina la silaba, ya que sale del area permitida
        else:
            newPositions.append((posiciones[i][0], posiciones[i][1]+1)) # agrega la posicion a la lista de nuevas posiciones
    del posiciones[:] # vacia la lista de posiciones
    posiciones.extend(newPositions) # le agrega a la lista de posiciones toda la lista de nuevas posiciones

def nuevaSilaba(silabas):
    return random.choice(silabas) # retorna un elemento random de la lista

def quitar(candidata, silabasEnPantalla, posiciones):
    silabasCandidatas = dameSilabas(candidata) # obtiene una lista con las silabas de la palabra candidata

    for silaba in silabasCandidatas: # recorre las silabas de la palabra
        if silaba in silabasEnPantalla: # si la silaba se encuentra en pantalla...
            posicion = silabasEnPantalla.index(silaba) # busca la posicion de la silaba en la lista de silabas en pantalal
            del silabasEnPantalla[posicion] # elimina la silaba
            del posiciones[posicion] # elimina la posicion de la silaba

def dameSilabas(candidata):
    return separador(candidata).split('-') # retorna una lista con todas las silabas de una palabra

def esValida(candidata, silabasEnPantalla, lemario):
    silabasCandidatas = dameSilabas(candidata) # obtiene una lista con las silabas de la palabra candidata

    if candidata not in lemario: # si la palabra candidata no se encuentra en el lemario...
        return False # retorna falso

    for silaba in silabasCandidatas: # recorre la lista de silabas candidatas
        if silaba not in silabasEnPantalla: # si una silaba no se encuentra en pantalla...
            return False # retorna falso

    return True # si ninguno de las casos anteriores se cumple, retorna true

def Puntos(candidata):
    total = 0

    for caracter in candidata: # recorre cada caracter de la palabra candidata
        if caracter in VOCALES: # si es vocal...
            total += 1
        elif caracter in DIFICILES: # si es un caracter "dificil"...
            total += 5
        else: # en cualquier otro caso...
            total += 2
    
    return total

def procesar(candidata, silabasEnPantalla, posiciones, lemario):
    if esValida(candidata, silabasEnPantalla, lemario): # si la palabra es valida...
        quitar(candidata, silabasEnPantalla, posiciones) # elimina la silaba de la pantalla
        return Puntos(candidata) # retorna la cantidad de puntos
    return 0 # si no es valida retorna 0 puntos

def randomNum(max):
    return random.random() * max # retorna un numero random con un maximo

def moverMenu(opciones, seleccionada, accion):
    if seleccionada == 0 and accion == -1: # si la opcion seleccionada es la primera y la accion es "subir"...
        return len(opciones) - 1 # retorna la ultima posicion de las opciones
    elif seleccionada == len(opciones) - 1 and accion == 1: # si la opcion seleccionada es la ultima y la accion es "bajar"...
        return 0 # retorna 0
    else: # en cualquier otro caso...
        return seleccionada + accion # retorna la opcion seleccionada + la accion (1 o -1)

# renderiza todas las opciones en el menu
def dibujarInicio(screen, opciones, opcionSeleccionada, jugador):
    defaultFont = pygame.font.Font( pygame.font.get_default_font(), 40)
    smallFont = pygame.font.Font( pygame.font.get_default_font(), 20)
    yInicial = 150

    screen.blit(smallFont.render("Jugador: " + jugador, 1, COLOR_TEXTO), (50, 50))

    for i in range(len(opciones)):
        posicion = (200, yInicial)

        if opciones[i] == opcionSeleccionada:
            screen.blit(defaultFont.render(opciones[i] + "*", 1, COLOR_LETRAS), posicion)
        else:
            screen.blit(defaultFont.render(opciones[i], 1, COLOR_TEXTO), posicion)

        yInicial += 100

# renderiza el puntaje final de un juego
def dibujarPuntajeJuego(screen, puntos):
    defaultFont = pygame.font.Font( pygame.font.get_default_font(), 40)

    screen.blit(defaultFont.render("PUNTAJE FINAL", 1, COLOR_TEXTO), (200, 150))
    screen.blit(defaultFont.render(str(puntos), 1, COLOR_LETRAS), (200, 250))

# renderiza la pantalla para ingresar el nombre del usuario
def dibujarIngresaNombre(screen, jugador):
    defaultFont = pygame.font.Font( pygame.font.get_default_font(), 40)
    smallFont = pygame.font.Font( pygame.font.get_default_font(), 20)

    screen.blit(defaultFont.render("INGRESA TU NOMBRE", 1, COLOR_TEXTO), (200, 150))
    screen.blit(defaultFont.render(jugador, 1, COLOR_LETRAS), (200, 250))
    screen.blit(smallFont.render("Presiona enter para continuar", 1, COLOR_TEXTO), (200, 450))

def procesarUsuario(jugador):
    if jugador == "": # valida que el nombre del jugador no este vacio
        return

    fileR = open("users.json", "r") # abre el archivo de usuarios
    data = json.load(fileR) # guarda el json de usuarios en la variable data

    if not jugador in data: # si el jugador no esta en la lista de usuarios
        data[jugador] = [] # crea el nuevo usuario

        fileW = open("users.json", "w") # abre el archivo de usuarios para escritura
        json.dump(data, fileW, indent=2) # escribe la nueva data en el json
        fileW.close()

    fileR.close()

def guardarPuntaje(jugador, puntos):
    fileR = open("users.json", "r") # abre el archivo de usuarios
    data = json.load(fileR) # guarda el json de usuarios en la variable data
    
    nuevoPuntaje = {} # crea el objeto de puntaje
    nuevoPuntaje['score'] = puntos # crea el "score" del puntaje
    nuevoPuntaje['date'] = datetime.now().strftime("%d/%m/%Y") # crea la fecha del puntaje

    data[jugador].append(nuevoPuntaje) # agrega a la lista del usuario el nuevo puntaje

    fileW = open("users.json", "w") # abre el archivo de usuarios para escritura
    json.dump(data, fileW, indent=2) # escribe la nueva data en el json

    fileW.close()
    fileR.close()

def buscarMejoresPuntajes(jugador):
    fileR = open("users.json", "r") # abre el archivo de usuarios
    data = json.load(fileR) # guarda el json de usuarios en la variable data

    return sorted(data[jugador], key=lambda x: x['score'], reverse=True) # ordena los puntajes de mayor a menor
    fileR.close()

# renderiza los 10 mejores puntajes
def dibujarPuntajes(screen, jugador, puntajes):
    defaultFont = pygame.font.Font( pygame.font.get_default_font(), 40)
    smallFont = pygame.font.Font( pygame.font.get_default_font(), 20)
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
