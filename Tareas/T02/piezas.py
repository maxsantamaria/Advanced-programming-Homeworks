from edd import *


class Pieza:
    def __init__(self, bordes):  # bordes es un string tipo 'GGGGGG'
        self.bordes = bordes
        self.id = bordes  # no cambia
        self.borde1 = bordes[0]
        self.borde2 = bordes[1]
        self.borde3 = bordes[2]
        self.borde4 = bordes[3]
        self.borde5 = bordes[4]
        self.borde6 = bordes[5]
        if (bordes == "CGGCGG" or
            bordes == ""):
            self.muralla = True
        self.grilla = False
        self.ciudad_separada = False
        if self.id == "CGGCGG" or self.id == "CRCCRC" or self.id == "CGGGCC":
            self.ciudad_separada = True  # para las piezas son 2 ciudades
        self.cerrada = False
        self.posicion = None  # Tupla
        self.bifurcacion = False
        if self.id == "GGPGPP" or self.id == "PPGPPG":
            self.bifurcacion = True

    def rotar_derecha(self):
        self.bordes = self.bordes[-1] + self.bordes[:5]
        self.actualizar_bordes()

    def rotar_izquierda(self):
        self.bordes = self.bordes[1:] + self.bordes[0]
        self.actualizar_bordes()

    def actualizar_bordes(self):
        self.borde1 = self.bordes[0]
        self.borde2 = self.bordes[1]
        self.borde3 = self.bordes[2]
        self.borde4 = self.bordes[3]
        self.borde5 = self.bordes[4]
        self.borde6 = self.bordes[5]


class Entidad:
    def __init__(self, tipo=None):
        self.piezas = ListaLigada()  # value = Pieza que conforma la entidad
        # tipo es un string: pasto(G), ciudad(C), camino(P), rio(R)
        self.tipo = tipo
        self.adyacentes = MySet()
        # adyacentes son las entidades que comparten piezas con esta entidad
        self.completa = False


class Pasto(Entidad):
    def __init__(self):
        super().__init__()


class Ciudad:
    def __init__(self):
        super().__init__()
        self.completa = False


class Camino:
    def __init__(self):
        super().__init__()


class Rio:
    def __init__(self):
        super().__init__()


with open("pieces_name.csv", "r") as file:
    lista_piezas = ListaLigada()
    for linea in file:
        linea = linea.strip()
        nueva_pieza = Pieza(linea)
        lista_piezas.append(nueva_pieza)

with open("pieces.csv", "r") as file:
    cantidad_piezas = Diccionario_Ligado()
    for linea in file:
        string_pieza, cantidad = linea.split(",")
        for pieza in lista_piezas:
            if pieza.bordes == string_pieza:
                cantidad_piezas.update(pieza.bordes, int(cantidad))

pieza1 = Pieza("ABCDEF")


