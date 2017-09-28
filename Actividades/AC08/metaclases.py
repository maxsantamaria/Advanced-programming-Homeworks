from functions import *

class MetaChess(type):
    def __call__(cls, *args, **kw):
        simbolos_piezas_j1 = []
        simbolos_piezas_j2 = []
        for pieza in args:
            if pieza.allied:
                simbolos_piezas_j1.append(pieza.letter)
            else:
                simbolos_piezas_j2.append(pieza.letter)
        peon_j1 = simbolos_piezas_j1.count("P")
        rey_j1 = simbolos_piezas_j1.count("R")
        reina_j1 = simbolos_piezas_j1.count("F")
        alfil_j1 = simbolos_piezas_j1.count("A")
        torre_j1 = simbolos_piezas_j1.count("T")
        caballo_j1 = simbolos_piezas_j1.count("C")
        peon_j2 = simbolos_piezas_j2.count("P")
        rey_j2 = simbolos_piezas_j2.count("R")
        reina_j2 = simbolos_piezas_j2.count("F")
        alfil_j2 = simbolos_piezas_j2.count("A")
        torre_j2 = simbolos_piezas_j2.count("T")
        caballo_j2 = simbolos_piezas_j2.count("C")
        if (peon_j1 != 8 or peon_j2 != 8 or rey_j1 != 1 or rey_j2 != 1
                or reina_j1 != 1 or reina_j2 != 1 or alfil_j1 != 2 or
                alfil_j2 != 2 or torre_j1 != 2 or torre_j2 != 2 or
                caballo_j1 != 2 or caballo_j2 != 2):
            return None


        if not hasattr(cls, "instance"):
            cls.instance = super().__call__(*args, **kw)
        else:
            return cls.instance



    def __new__(cls, nombre, base_clases, diccionario):
        def recibir_pieza(func):
            def _recibir_pieza(*args):
                func()
                for arg in args:
                    diccionario["add_piece"](arg)
                return func
            return _recibir_pieza
        diccionario["__init__"] = recibir_pieza(diccionario["__init__"])
        diccionario["valid_move"] = chess_valid_move
        return super().__new__(cls, nombre, base_clases, diccionario)


    def __init__(cls, nombre, base_clases, diccionario):
        pass


class MetaPiece(type):
    simbolos_piezas_j1 = []
    simbolos_piezas_j2 = []

    def __call__(cls, *args, **kwargs):
        letra = cls.__name__
        if len(kwargs) == 0:
            jugador = True
        else:
            jugador = False
        peon_j1 = MetaPiece.simbolos_piezas_j1.count("Peon")
        rey_j1 = MetaPiece.simbolos_piezas_j1.count("Rey")
        reina_j1 = MetaPiece.simbolos_piezas_j1.count("Reina")
        alfil_j1 = MetaPiece.simbolos_piezas_j1.count("Alfil")
        torre_j1 = MetaPiece.simbolos_piezas_j1.count("Torre")
        caballo_j1 = MetaPiece.simbolos_piezas_j1.count("Caballo")
        peon_j2 = MetaPiece.simbolos_piezas_j2.count("Peon")
        rey_j2 = MetaPiece.simbolos_piezas_j2.count("Rey")
        reina_j2 = MetaPiece.simbolos_piezas_j2.count("Reina")
        alfil_j2 = MetaPiece.simbolos_piezas_j2.count("Alfil")
        torre_j2 = MetaPiece.simbolos_piezas_j2.count("Torre")
        caballo_j2 = MetaPiece.simbolos_piezas_j2.count("Caballo")
        if jugador:
            if letra == "Peon" and peon_j1 >= 8:
                return None
            elif letra == "Rey" and rey_j1 >= 1:
                return None
            elif letra == "Reina" and reina_j1 >= 1:
                return None
            elif letra == "Alfil" and alfil_j1 >= 2:
                return None
            elif letra == "Torre" and torre_j1 >= 2:
                return None
            elif letra == "Caballo" and caballo_j1 >= 2:
                return None
            MetaPiece.simbolos_piezas_j1.append(letra)
        elif not jugador:
            if letra == "Peon" and peon_j2 >= 8:
                return None
            elif letra == "Rey" and rey_j2 >= 1:
                return None
            elif letra == "Reina" and reina_j2 >= 1:
                return None
            elif letra == "Alfil" and alfil_j2 >= 2:
                return None
            elif letra == "Torre" and torre_j2 >= 2:
                return None
            elif letra == "Caballo" and caballo_j2 >= 2:
                return None
            MetaPiece.simbolos_piezas_j2.append(letra)

        return super().__call__(*args, **kwargs)

    def __new__(cls, nombre, base_clases, diccionario):
        name = cls.__name__
        if name == "Peon":
            diccionario["valid_move"] = peon_valid_move
        elif name == "Caballo":
            diccionario["valid_move"] = caballo_valid_move
        elif name == "Torre":
            diccionario["valid_move"] = torre_valid_move
        elif name == "Rey":
            diccionario["valid_move"] = rey_valid_move
        elif name == "Alfil":
            diccionario["valid_move"] = alfil_valid_move
        elif name == "Reina":
            diccionario["valid_move"] = reina_valid_move
        return super().__new__(cls, nombre, base_clases, diccionario)