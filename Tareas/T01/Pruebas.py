from time import strftime, gmtime
from Order import *
from decimal import Decimal as d
from User import *
import datetime as DT
from csv_reader import *

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
a = d("5")
a = str(a)
print(type(a))
a = "   hola como estas "
print(a.strip())


lista1 = [2, 3, 4, 5]

for elem in lista1:
    print(elem)
    if 3 in lista1:
        lista1.remove(3)

if True:
    print("hola")
    pass
    print("chao")

fecha1 = Fecha(2000, 10, 5)
fecha2 = Fecha(3000, 10, 3)
fecha3 = Fecha(3000, 5, 3)
myList = [fecha1, fecha2, fecha3]
nueva_lista = list(filter(lambda x: x.año == 3000, myList))
for elem in nueva_lista:
    print(elem.mes)

print(len(nueva_lista))

usuario1 = Usuario("maxam", "max", "santa", "")
#while usuario1.nacimiento == "":
#    nac = input("Nac: ")
#    usuario1.nacimiento = nac

today = DT.date.today()
week_ago = today - DT.timedelta(days=7)

print(today, week_ago)

a = (1, 2)
b = (3, 4)

print(a+b)

diccio = {1 : "max", 2 : "mex"}
string = str(diccio)
print(string)

balance = "DCC : 50000, BAN : 30000"
print(dict(e.split(" : ") for e in balance.split(",") ))

a = set()
a.add(5)
a.add(6)
b = list(a)
print(b, a)

