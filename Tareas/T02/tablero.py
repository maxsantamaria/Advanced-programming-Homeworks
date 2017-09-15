from edd import *
from piezas import *
from jugadores import *


class Tablero:
    def __init__(self):
        self.elementos = Diccionario_Ligado()  # key = tupla, value = Pieza
        for i in range(0, 8):
            for j in range(0, 8):
                posicion = Tupla(i, j)
                self.elementos.update(posicion, None)

    def pieza_completada(self, pieza, jugador_actual, simulacion, *args):
        # cuando simulacion es True, da lo mismo que las piezas pertenezcan
        # al mismo jugador
        up, down, upright, upleft, dright, dleft = args
        try:
            conect = self.elementos[up]
            if pieza.borde1 == "C":
                if conect and conect.borde4 == pieza.borde1 and \
                                up in jugador_actual.movimientos:
                        # para saber si la pieza se une a otra del mismo
                        # jugador
                    pieza.cerrada = True
                elif conect and conect.borde4 == pieza.borde1 and simulacion:
                    pieza.cerrada = True
                else:
                    pieza.cerrada = False
                    return
        except KeyError:  # grilla se considera como "muro"
            pieza.cerrada = True
        try:
            conect = self.elementos[upright]
            if pieza.borde2 == "C":
                if conect and conect.borde5 == pieza.borde2 and\
                                upright in jugador_actual.movimientos:
                        # para saber si la pieza se une a otra del mismo
                        # jugador
                    pieza.cerrada = True
                elif conect and conect.borde5 == pieza.borde2 and simulacion:
                    pieza.cerrada = True
                else:
                    pieza.cerrada = False
                    return
        except KeyError:  # grilla
            pieza.cerrada = True
        try:
            conect = self.elementos[dright]
            if pieza.borde3 == "C":
                if conect and conect.borde6 == pieza.borde3 and \
                                dright in jugador_actual.movimientos:
                        # para saber si la pieza se une a otra del mismo
                        # jugador
                    pieza.cerrada = True
                elif conect and conect.borde6 == pieza.borde3 and simulacion:
                    pieza.cerrada = True
                else:
                    pieza.cerrada = False
                    return
        except KeyError:
            pieza.cerrada = True
        try:
            conect = self.elementos[down]
            if pieza.borde4 == "C":
                if conect and conect.borde1 == pieza.borde4 and \
                                down in jugador_actual.movimientos:
                        # para saber si la pieza se une a otra del mismo
                        # jugador
                    pieza.cerrada = True
                elif conect and conect.borde1 == pieza.borde4 and simulacion:
                    pieza.cerrada = True
                else:
                    pieza.cerrada = False
                    return
        except KeyError:
            pieza.cerrada = True
        try:
            conect = self.elementos[dleft]
            if pieza.borde5 == "C":
                if conect and conect.borde2 == pieza.borde5 and \
                                dleft in jugador_actual.movimientos:
                        # para saber si la pieza se une a otra del mismo
                        # jugador
                    pieza.cerrada = True
                elif conect and conect.borde2 == pieza.borde5 and simulacion:
                    pieza.cerrada = True
                else:
                    pieza.cerrada = False
                    return
        except KeyError:
            pieza.cerrada = True
        try:
            conect = self.elementos[upleft]
            if pieza.borde6 == "C":
                if conect and conect.borde3 == pieza.borde6 and \
                                upleft in jugador_actual.movimientos:
                        # para saber si la pieza se une a otra del mismo
                        # jugador
                    pieza.cerrada = True
                elif conect and conect.borde3 == pieza.borde6 and simulacion:
                    pieza.cerrada = True
                else:
                    pieza.cerrada = False
                    return
        except KeyError:
            pieza.cerrada = True
