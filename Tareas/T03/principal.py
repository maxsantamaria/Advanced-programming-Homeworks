from reader import *
from fenotipo import *
from functools import reduce
from itertools import groupby
from collections import namedtuple
import sys
import time


def procesar_linea(line):
    line.strip()
    nombre, lim_superior = obtener_nombre(line)
    line = line[lim_superior:]
    apellido, lim_superior = obtener_nombre(line)
    nombre = nombre + " " + apellido
    line = line[lim_superior:]
    caracteristicas2 = obtener_caracteristicas(line)

    ultimo_numero = line.rfind(caracteristicas2[-1])
    parte_caracteristicas = line[:ultimo_numero + len(caracteristicas2[-1])]
    tags = ["".join(x) for letra, x in
            groupby(parte_caracteristicas, key=str.isalpha) if letra]

    # parte genoma:
    line = line[ultimo_numero + len(caracteristicas2[-1]):]

    #caracteristicas = {tupla[0]: conectar_genoma_listas(tupla[1],
    #                                                    obtener_genoma
    #                                                    (line),
    #                                                    listas)
    #                   for tupla in zip(tags, caracteristicas2)}

    caracteristicas = {tupla[0]: conectar_genoma_listas2(tupla[1],
                                                        line,
                                                        listas)
                       for tupla in zip(tags, caracteristicas2)}
    return Persona(nombre, apellido, "", caracteristicas)

parser1 = lambda line: line.strip().split(";")
parser2 = lambda string: string.strip().split(",")
with open("listas.txt", "r", encoding="utf-8") as file2:
    listas = {linea.strip().split(";"): linea.strip().split()}
    listas = {parser1(linea)[0]: parser2(parser1(linea)[1]) for linea in file2}

Persona = namedtuple("Persona", ["nombre", "apellido",
                                 "genoma", "caracteristicas"])
# nombre: str
# apellido: str
# genoma: lista de genes
# caracteristicas: list of dict key = Tag caracteristica, value = lista_genes


with open("genomas.txt", "r", encoding="utf-8") as file1:
    print("empieza")
    tiempo_empieza = time.time()
    personas = list(map(procesar_linea, (line for line in file1)))
    for linea in file1:
        pass
    print("termina", time.time() - tiempo_empieza)

print(personas)
#raise TypeError

#conectar_genoma_listas(personas[1], listas)
#print(personas[0].caracteristicas)


#### FENOTIPO

parser_tag_caract = {"AAG": "Altura",
                     "GTC": "Color de ojos",
                     "GGA": "Color de pelo",
                     "TCT": "Tono de piel",
                     "GTA": "Forma de la nariz",
                     "CTC": "Tamaño de los pies",
                     "CGA": "Donde hay vello corporal",
                     "TGG": "Tamaño de la guata",
                     "TAG": "Problemas de visión"}


deterministas = ("GTC", "GGA", "GTA")

ojos = map(determinar_ojos, obtener_genes(personas, "GTC"))
pelos = map(determinar_pelo, obtener_genes(personas, "GGA"))
narices = map(determinar_nariz, obtener_genes(personas, "GTA"))

alturas = map(determinar_altura, obtener_genes(personas, "AAG"))
pies = map(determinar_pies, obtener_genes(personas, "CTC"))
pieles = map(determinar_piel, obtener_genes(personas, "TCT"))
guatas = map(determinar_guata, obtener_genes(personas, "TGG"))

vellos = map(determinar_vello, obtener_genes(personas, "CGA"))
visiones = map(determinar_vision, obtener_genes(personas, "TAG"))

Persona_con_fenotipo = namedtuple("Persona", ["nombre", "apellido", "genoma",
                                              "caracteristicas", "altura",
                                              "ojo", "pelo", "piel", "nariz",
                                              "pie", "vello","guata", "vision"
                                              ])

#with open("fenotipos_nuevos.txt", "w", encoding="utf-8") as file:
#    file.write("Nombre, ojos, pelos, narices, altura, pie, piel, guatas, vellos, vision\n")
#    for args in zip(personas, ojos, pelos, narices, alturas, pies, pieles,
#                guatas, vellos, visiones):
    # ojo, pelo, nariz, altura, pie, piel, guata, vello, vision
        #print(args)
#        file.write(args[0].nombre + ", ")
#        for arg in args[1:]:
#            file.write(str(arg) + ", ")
#        file.write("\n")


#raise TypeError
personas = [Persona_con_fenotipo(args[0].nombre, args[0].apellido,
                                 args[0].genoma, args[0].caracteristicas,
                                 *args[1:])
            for args in zip(personas, alturas, ojos, pelos, pieles, narices,
                            pies, vellos, guatas, visiones)]

#parientes_grado_1 = map(determinar_grado_1, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))

#parientes_gradon = map(determinar_grado_n, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))

#parientes_grado0 = map(determinar_grado0, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))

#parientes_grado1 = map(determinar_grado1, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))

#parientes_grado2 = map(determinar_grado2, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))




a = ["".join(x) for _, x in groupby("dfsd98sd8f68as7df56", key=str.isdigit) if _ == True]
print(a)
for elem in groupby("hola2chao3", key=str.isdigit):
    print("".join(elem[1]))

for persona in personas:
    print(persona)
#print("TAMAÑOOOO", sys.getsizeof(personas))