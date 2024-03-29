from collections import namedtuple
import pygame

TAMANNO_LETRA = 20
FPS_inicial = 30
TIEMPO_MAX = 60

ANCHO = 800
ALTO = 600
COLOR_LETRAS = (20,200,20)
COLOR_FONDO = (56,12,42)
COLOR_TEXTO = (255,255,255)
COLOR_TIEMPO_FINAL = (200,20,10)
Punto = namedtuple("Punto","x y")

VOCALES = "aeiou"
DIFICILES = "jkqwxyz"

PANTALLA_JUEGO = "PANTALLA_JUEGO"
PANTALLA_INICIO = "PANTALLA_INICIO"
PANTALLA_PUNTAJES = "PANTALLA_PUNTAJES"

TECLA_ARRIBA = [1073741906, 273]
TECLA_ABAJO = [1073741905, 274]
TECLA_ENTER = 13
