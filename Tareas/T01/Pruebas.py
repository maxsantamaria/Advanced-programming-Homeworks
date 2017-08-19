from time import strftime, gmtime
from Order import *
from decimal import Decimal as d
print(strftime("%Y-%m-%d ", gmtime()))

lista = [5, 1, 3]
print(min(lista), max(lista))

dicc = {}
dicc.update({"hola" : "max"})
print(dicc)

dicc = [{"primero":21, 3:4}, {"primero" : 3, 50 : 5}, {"primero": 1, 5 : 2}]

dicc2 = sorted(dicc, key = lambda elem : elem["primero"])

print(dicc2)

lista_orders = []


class Hola:
    def hola(self):
        pass

h = Hola()

print(type(object))

class Fecha:
    def __init__(self, año, mes, dia):
        self.año = año
        self.mes = mes
        self.dia = dia


mejores_opciones = [Fecha(2015, 10, 5), Fecha(2014, 5, 2), Fecha(2015, 1, 6), Fecha(2015, 10, 4)]

mejores_opciones.sort(key=lambda elem: (int(elem.año), int(elem.mes), int(elem.dia)))
for opcion in mejores_opciones:
    print(opcion.dia)

print(5 + d("5"))
print(5 != d("5"))