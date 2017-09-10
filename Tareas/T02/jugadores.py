from edd import *


class Jugador:
    def __init__(self, numero, color):
        self.numero = numero
        self.color = color
        self.movimientos = ListaLigada()  # guardara las posiciones usadas
        self.puntaje = 0
        self.piezas = ListaLigada()
        self.entidades = ListaLigada()