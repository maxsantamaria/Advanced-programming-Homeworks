from collections import namedtuple


class Persona:
    def __init__(self, nombre, apellido, edad, sexo, ciudad, oficio, sueldo):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.sexo = sexo
        self.ciudad = ciudad
        self.oficio = oficio
        self.sueldo = sueldo


parser = lambda line: line.strip().split(",")
with open("Informacion_personas.txt", "r", encoding='utf-8') as file:
    personas = [Persona(*parser(linea)) for linea in file]

#print(len(personas), personas[0].nombre)

Pais = namedtuple("Pais", ["sigla", "nombre"])
with open("paises.txt", "r", encoding='utf-8') as file:
    paises = {parser(linea)[0]: parser(linea)[1] for linea in file}
    paises = [Pais(*parser(linea)) for linea in file]

#print(len(paises), paises["CN"])

Ciudad = namedtuple("Ciudad", ["sigla_pais", "nombre"])
with open("ciudades.txt", "r", encoding='utf-8') as file:
    ciudades = [Ciudad(*parser(linea)) for linea in file]

print(ciudades[0].pais)
