from reader import *
from fenotipo import *


parser1 = lambda line: line.strip().split(";")
parser2 = lambda string: string.strip().split(",")
with open("listas.txt", "r", encoding="utf-8") as file2:
    listas = {parser1(linea)[0]: parser2(parser1(linea)[1]) for linea in file2}

Persona = namedtuple("Persona", ["nombre", "apellido",
                                 "genoma", "caracteristicas"])
# nombre: str
# apellido: str
# genoma: lista de genes
# caracteristicas: list of dict key = Tag caracteristica, value = lista_genes
with open("genomas.txt", "r", encoding="utf-8") as file1:
    personas = []
    for line in file1:
        nombre, lim_superior = obtener_nombre(line)
        line = line[lim_superior:]
        apellido, lim_superior = obtener_nombre(line)
        line = line[lim_superior:]
        letras = [char for char in line if char.isalpha()]
        tags = "".join(letras[:9*3])
        #print(tags)
        tags = [tags[i: i + 3] for i in range(len(tags)) if i % 3 == 0]
        #print(tags)
        #caracteristicas = obtener_caracteristicas(line)
        caracteristicas2 = obtener_caracteristicas_rec(line)
        #print(caracteristicas)
        #print(caracteristicas2, "\n")
        genoma = obtener_genoma(letras)
        #caracteristicas = {caracteristica:
        #                       conectar_genoma_listas(id, genoma, listas)
        #                   for caracteristica, id in caracteristicas.items()}
        caracteristicas = {tupla[0]: conectar_genoma_listas(tupla[1], genoma, listas) for tupla in zip(tags, caracteristicas2)}
        #print(caracteristicas, "a")
        #print(caracteristicas2, "b")
        personas.append(Persona(nombre, apellido, genoma, caracteristicas))

#print(personas)


#conectar_genoma_listas(personas[1], listas)
#print(personas[0].caracteristicas)
