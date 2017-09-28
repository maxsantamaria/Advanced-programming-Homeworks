from functions import *
from pieces import *

class MetaChess(type):
    def __call__(cls, *args, **kw):
        for pieza in args:
            if not isinstance(pieza, PiezaAjedrez):
                return None


        if not hasattr(cls, "instance"):
            cls.instance = super().__call__(*args, **kw)
        else:
            return cls.instance



    def __new__(cls, nombre, base_clases, diccionario):
        def recibir_pieza(func):
            def _recibir_pieza(*args):
                func(*args)
                for arg in args:
                    diccionario["add_piece"](arg)
                return func
            return _recibir_pieza
        diccionario["__init__"] = recibir_pieza(diccionario["__init__"])
        diccionario["valid_move"] = chess_valid_move
        return super().__new__(cls, nombre, base_clases, diccionario)




class MetaPiece(type):
    simbolos_piezas_j1 = []
    simbolos_piezas_j2 = []
    ultima_pieza = None

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
                return MetaPiece.ultima_pieza
            elif letra == "Rey" and rey_j1 >= 1:
                return MetaPiece.ultima_pieza
            elif letra == "Reina" and reina_j1 >= 1:
                return MetaPiece.ultima_pieza
            elif letra == "Alfil" and alfil_j1 >= 2:
                return MetaPiece.ultima_pieza
            elif letra == "Torre" and torre_j1 >= 2:
                return MetaPiece.ultima_pieza
            elif letra == "Caballo" and caballo_j1 >= 2:
                return MetaPiece.ultima_pieza
            MetaPiece.simbolos_piezas_j1.append(letra)
        elif not jugador:
            if letra == "Peon" and peon_j2 >= 8:
                return MetaPiece.ultima_pieza
            elif letra == "Rey" and rey_j2 >= 1:
                return MetaPiece.ultima_pieza
            elif letra == "Reina" and reina_j2 >= 1:
                return MetaPiece.ultima_pieza
            elif letra == "Alfil" and alfil_j2 >= 2:
                return MetaPiece.ultima_pieza
            elif letra == "Torre" and torre_j2 >= 2:
                return MetaPiece.ultima_pieza
            elif letra == "Caballo" and caballo_j2 >= 2:
                return MetaPiece.ultima_pieza
            MetaPiece.simbolos_piezas_j2.append(letra)
        Pieza = super().__call__(*args, **kwargs)
        MetaPiece.ultima_pieza = Pieza
        return Pieza

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