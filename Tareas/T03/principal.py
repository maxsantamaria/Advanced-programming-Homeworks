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
        nombre = nombre + " " + apellido
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

#with open("fenotipos.txt", "w", encoding="utf-8") as file:
#    file.write("Nombre, ojos, pelos, narices, altura, pie, piel, guatas, vellos, vision\n")
#    for args in zip(personas, ojos, pelos, narices, alturas, pies, pieles,
#                guatas, vellos, visiones):
    # ojo, pelo, nariz, altura, pie, piel, guata, vello, vision
        #print(args)
#        file.write(args[0].nombre + ", ")
#        for arg in args[1:]:
#            file.write(str(arg) + ", ")
#        file.write("\n")


personas = [Persona_con_fenotipo(args[0].nombre, args[0].apellido,
                                 args[0].genoma, args[0].caracteristicas,
                                 *args[1:])
            for args in zip(personas, alturas, ojos, pelos, pieles, narices,
                            pies, vellos, guatas, visiones)]

print("\nGrado -1")
parientes_grado_1 = map(determinar_grado_1, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))
parientes_grado_1 = [parientes for lista in parientes_grado_1 for parientes in lista]
for parientes in parientes_grado_1:
    print(parientes)

print("\nGrado n")
parientes_gradon = map(determinar_grado_n, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))
parientes_gradon = [parientes for lista in parientes_gradon for parientes in lista]
for parientes in parientes_gradon:
    print(parientes[0].nombre, parientes[1].nombre)

print("\nGrado 0")
parientes_grado0 = map(determinar_grado0, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))
parientes_grado0 = [parientes for lista in parientes_grado0 for parientes in lista]
for parientes in parientes_grado0:
    print(parientes[0].nombre, parientes[1].nombre)

print("\nGrado 1")
parientes_grado1 = map(determinar_grado1, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))
parientes_grado1 = [parientes for lista in parientes_grado1 for parientes in lista]
for parientes in parientes_grado1:
    print(parientes[0].nombre, parientes[1].nombre)

print("\nGrado 2")
parientes_grado2 = map(determinar_grado2, ((persona, filter(lambda x: x != persona, personas)) for persona in personas))
parientes_grado2 = [parientes for lista in parientes_grado2 for parientes in lista]
for parientes in parientes_grado2:
    print(parientes[0].nombre, parientes[1].nombre)


Persona_con_pariente = namedtuple("Persona", ["nombre", "apellido", "genoma",
                                              "caracteristicas", "ojo", "pelo",
                                              "nariz", "altura", "pie", "piel",
                                              "guata", "vello", "vision",
                                              "grado_1", "grado0", "grado1",
                                              "grado2", "gradon"])





