from excepciones import *
#from principal import personas
from reader import *
from functools import reduce
from itertools import groupby
import sys
import time
from collections import namedtuple


# Decoradores
def determinar_errores_genoma(func):
    def _determinar_errores_genoma(*args):  # args son los genes como dicc
        genes = args[0]
        #print(genes.keys())
        letras = map(letra_aceptada, genes.keys())
        if False in letras:
            return None
        return func(*args)
    return _determinar_errores_genoma

def letra_aceptada(triplete):
    aceptadas = ["A", "C", "G", "T"]
    control = (letra in aceptadas for letra in triplete)
    if False in control:
        return False
    return True

# Fin decoradores


def obtener_genes(persons, tag_buscado):
    genes = (genes for persona in persons
             for tag, genes in persona.caracteristicas.items()
             if tag == tag_buscado)
    return genes


@determinar_errores_genoma
def determinar_ojos(genes):
    # old genes: list de genes (3 letras cada uno) de una caracteristica
    # new genes: dicc con key = Triplete, value = Cantidad que aparece
    # en genoma
    if "CCT" in genes.keys():
        return "cafes"
    elif "AAT" in genes.keys():
        return "azules"
    elif "CAG" in genes.keys():
        return "verdes"


@determinar_errores_genoma
def determinar_pelo(genes):
    # genes: list de genes (3 letras cada uno) de una caracteristica
    if "GTG" in genes:
        return "negro"
    elif "AAT" in genes:
        return "rubio"
    elif "CCT" in genes:
        return "pelirrojo"


@determinar_errores_genoma
def determinar_nariz(genes):
    # genes: list de genes (3 letras cada uno) de una caracteristica
    if "TCG" in genes:
        return "aguileña"
    elif "CAG" in genes:
        return "respingada"
    elif "TAC" in genes:
        return "recta"


@determinar_errores_genoma
def determinar_altura(genes):
    alta = genes["AGT"]
    baja = genes["ACT"]
    porcentaje = alta / (alta + baja)
    altura = 1.40 + 0.70 * porcentaje
    return altura


@determinar_errores_genoma
def determinar_pies(genes):
    grandes = genes["GTA"]
    chicos = genes["CCA"]
    porcentaje = grandes / (grandes + chicos)
    pies = 34 + 14 * porcentaje
    return pies


@determinar_errores_genoma
def determinar_piel(genes):
    clara = genes["AAT"]
    oscura = genes["GCG"]
    porcentaje = clara / (clara + oscura)
    if porcentaje >= 0.75:
        return "albino"
    elif 0.5 <= porcentaje < 0.75:
        return "blanco"
    elif 0.25 <= porcentaje < 0.5:
        return "moreno"
    elif porcentaje < 0.25:
        return "negro"


@determinar_errores_genoma
def determinar_guata(genes):
    chica = genes["ACT"]
    grande = genes["AGT"]
    porcentaje = chica / (chica + grande)
    if porcentaje >= 0.75:
        return "modelo"
    elif 0.5 <= porcentaje < 0.75:
        return "atleta"
    elif 0.25 <= porcentaje < 0.5:
        return "dieta"
    elif porcentaje < 0.25:
        return "guaton"


@determinar_errores_genoma
def determinar_vello(genes):
    pecho = genes["TGC"]
    axila = genes["GTG"]
    espalda = genes["CCT"]
    vello = tuple()
    try:
        if pecho / (pecho + axila + espalda) >= 0.2:
            vello += tuple(["pecho"])
        if axila / (pecho + axila + espalda) >= 0.2:
            vello += tuple(["axila"])
        if espalda / (pecho + axila + espalda) >= 0.2:
            vello += tuple(["espalda"])
    except ZeroDivisionError:
        pass
    return vello


@determinar_errores_genoma
def determinar_vision(genes):
    daltonismo = genes["TTC"]
    miopia = genes["ATT"]
    problemas_vision = tuple()
    try:
        porcentaje_daltonismo = daltonismo / (daltonismo + miopia)
        porcentaje_miopia = miopia / (daltonismo + miopia)
        if porcentaje_daltonismo >= 0.2:
            problemas_vision += tuple(["daltonismo"])
        if porcentaje_miopia >= 0.2:
            problemas_vision += tuple(["miopia"])
    except ZeroDivisionError:
        pass
    return problemas_vision


def determinar_grado_1(args):  # namedtuple, list
    persona = args[0]
    resto_personas = args[1]
    control_error_grado0()
    parientes = [(persona, pariente) for pariente in resto_personas
                 if persona.ojo != pariente.ojo and
                 persona.pelo != pariente.pelo and
                 persona.nariz != pariente.nariz and
                 persona.altura != pariente.altura and
                 persona.pie != pariente.pie and
                 persona.piel != pariente.piel and
                 persona.guata != pariente.guata and
                 persona.vello != pariente.vello and
                 persona.vision != pariente.vision]
    return parientes


def determinar_diferencia_guata(guata1, guata2):
    grados = ["modelo", "atleta", "dieta", "guaton"]
    grado1 = grados.index(guata1)
    grado2 = grados.index(guata2)
    diferencia = abs(grado1 - grado2)
    if diferencia <= 1:
        return True
    else:
        return False


def determinar_grado_n(args):
    persona = args[0]
    resto_personas = args[1]
    control_error_gradon()
    parientes = [(persona, pariente) for pariente in resto_personas
                 if abs(persona.altura - pariente.altura) <= 0.7 and
                 persona.piel == pariente.piel and
                 abs(persona.pie - pariente.pie) <= 6 and
                 determinar_diferencia_guata(persona.guata, pariente.guata)]
    return parientes


def determinar_grado0(args):  # namedtuple, list
    persona = args[0]
    resto_personas = args[1]
    control_error_grado0()
    parientes = [(persona, pariente) for pariente in resto_personas
                 if persona.ojo == pariente.ojo and
                 persona.pelo == pariente.pelo and
                 persona.nariz == pariente.nariz and
                 persona.altura == pariente.altura and
                 persona.pie == pariente.pie and
                 persona.piel == pariente.piel and
                 persona.guata == pariente.guata and
                 persona.vello == pariente.vello and
                 persona.vision == pariente.vision]
    return parientes


def determinar_grado1(args):  # namedtuple, list
    persona = args[0]
    resto_personas = args[1]
    control_error_grado1()

    parientes = [(persona, pariente) for pariente in resto_personas
                 if persona.ojo == pariente.ojo and
                 persona.pelo == pariente.pelo and
                 persona.nariz == pariente.nariz and
                 abs(persona.altura - pariente.altura) <= 0.20 and
                 abs(persona.pie - pariente.pie) <= 2 and
                 persona.piel == pariente.piel and
                 persona.vision == pariente.vision]
    return parientes


def determinar_grado2(args):  # namedtuple, list of namedtuples
    persona = args[0]
    resto_personas = args[1]
    control_error_grado2()
    parientes = [(persona, pariente) for pariente in resto_personas
                 if persona.pelo == pariente.pelo and
                 abs(persona.altura - pariente.altura) <= 0.5 and
                 abs(persona.pie - pariente.pie) <= 4 and
                 persona.piel == pariente.piel and
                 persona.vision == pariente.vision]
    return parientes


def control_error_grado2():
    # se hace para controlar la consulta pariente de
    pelos = map(determinar_pelo, obtener_genes(personas, "GGA"))
    alturas = map(determinar_altura, obtener_genes(personas, "AAG"))
    pies = map(determinar_pies, obtener_genes(personas, "CTC"))
    pieles = map(determinar_piel, obtener_genes(personas, "TCT"))
    visiones = map(determinar_vision, obtener_genes(personas, "TAG"))
    if None in pelos or None in alturas or None in pies or None in visiones\
            or None in pieles:
        raise GenomeError


def control_error_grado1():
    # se hace para controlar la consulta pariente de
    ojos = map(determinar_ojos, obtener_genes(personas, "GTC"))
    pelos = map(determinar_pelo, obtener_genes(personas, "GGA"))
    narices = map(determinar_nariz, obtener_genes(personas, "GTA"))
    alturas = map(determinar_altura, obtener_genes(personas, "AAG"))
    pies = map(determinar_pies, obtener_genes(personas, "CTC"))
    pieles = map(determinar_piel, obtener_genes(personas, "TCT"))
    visiones = map(determinar_vision, obtener_genes(personas, "TAG"))
    if None in pelos or None in alturas or None in pies or None in visiones \
            or None in narices or None in ojos or None in pieles:
        raise GenomeError


def control_error_grado0():
    # se hace para controlar la consulta pariente de
    ojos = map(determinar_ojos, obtener_genes(personas, "GTC"))
    pelos = map(determinar_pelo, obtener_genes(personas, "GGA"))
    narices = map(determinar_nariz, obtener_genes(personas, "GTA"))
    alturas = map(determinar_altura, obtener_genes(personas, "AAG"))
    pies = map(determinar_pies, obtener_genes(personas, "CTC"))
    pieles = map(determinar_piel, obtener_genes(personas, "TCT"))
    guatas = map(determinar_guata, obtener_genes(personas, "TGG"))
    vellos = map(determinar_vello, obtener_genes(personas, "CGA"))
    visiones = map(determinar_vision, obtener_genes(personas, "TAG"))
    if None in pelos or None in alturas or None in pies or None in visiones \
            or None in narices or None in ojos or None in guatas\
            or None in vellos or None in pieles:
        raise GenomeError


def control_error_gradon():
    # se hace para controlar la consulta pariente de
    pelos = map(determinar_pelo, obtener_genes(personas, "GGA"))
    alturas = map(determinar_altura, obtener_genes(personas, "AAG"))
    pies = map(determinar_pies, obtener_genes(personas, "CTC"))
    pieles = map(determinar_piel, obtener_genes(personas, "TCT"))
    guatas = map(determinar_guata, obtener_genes(personas, "TGG"))
    if None in pelos or None in alturas or None in pies \
            or None in guatas\
            or None in pieles:
        raise GenomeError


def abrir_genomas(archivo):
    personas = list(map(procesar_linea, (line for line in archivo)))
    ojos, pelos, narices, alturas,\
        pies, pieles, guatas, vellos, visiones = determinar_fenotipos(personas)
    Persona_con_fenotipo = namedtuple("Persona",
                                      ["nombre", "apellido", "genoma",
                                       "caracteristicas", "altura",
                                       "ojo", "pelo", "piel", "nariz",
                                       "pie", "vello", "guata", "vision"
                                       ])
    personas = [Persona_con_fenotipo(args[0].nombre, args[0].apellido,
                                     args[0].genoma,
                                     args[0].caracteristicas,
                                     *args[1:])
                for args in
                zip(personas, alturas, ojos, pelos, pieles, narices,
                    pies, vellos, guatas, visiones)]
    return personas


def determinar_fenotipos(personas):
    ojos = map(determinar_ojos, obtener_genes(personas, "GTC"))
    pelos = map(determinar_pelo, obtener_genes(personas, "GGA"))
    narices = map(determinar_nariz, obtener_genes(personas, "GTA"))
    alturas = map(determinar_altura, obtener_genes(personas, "AAG"))
    pies = map(determinar_pies, obtener_genes(personas, "CTC"))
    pieles = map(determinar_piel, obtener_genes(personas, "TCT"))
    guatas = map(determinar_guata, obtener_genes(personas, "TGG"))
    vellos = map(determinar_vello, obtener_genes(personas, "CGA"))
    visiones = map(determinar_vision, obtener_genes(personas, "TAG"))
    return ojos, pelos, narices, alturas, pies, pieles, guatas, vellos, \
        visiones


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
    caracteristicas = {tupla[0]: conectar_genoma_listas2(tupla[1],
                                                         line,
                                                         listas)
                       for tupla in zip(tags, caracteristicas2)}
    return Persona(nombre, apellido, "", caracteristicas)


def parser1(line):
    return line.strip().split(";")


def parser2(line):
    return line.strip().split(",")


parser_tag_caract = {"AAG": "Altura",
                     "GTC": "Color de ojos",
                     "GGA": "Color de pelo",
                     "TCT": "Tono de piel",
                     "GTA": "Forma de la nariz",
                     "CTC": "Tamaño de los pies",
                     "CGA": "Donde hay vello corporal",
                     "TGG": "Tamaño de la guata",
                     "TAG": "Problemas de visión"}

with open("listas.txt", "r", encoding="utf-8") as file2:
    listas = {parser1(linea)[0]: parser2(parser1(linea)[1]) for linea in file2}

Persona = namedtuple("Persona", ["nombre", "apellido",
                                 "genoma", "caracteristicas"])
# nombre: str
# apellido: str
# genoma: lista de genes
# caracteristicas: list of dict key = Tag caracteristica, value = lista_genes


with open("genoma.txt", "r", encoding="utf-8") as file1:
    print("empieza")
    tiempo_empieza = time.time()
    personas = list(map(procesar_linea, (line for line in file1)))
    print("termina", time.time() - tiempo_empieza)

# FENOTIPO

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
                                              "pie", "vello", "guata", "vision"
                                              ])

# with open("fenotipos_nuevos.txt", "w", encoding="utf-8") as file:
#    file.write("Nombre, ojos, pelos, narices, altura, pie, piel, guatas,
#               vellos, vision\n")
#    for args in zip(personas, ojos, pelos, narices, alturas, pies, pieles,
#                guatas, vellos, visiones):
# ojo, pelo, nariz, altura, pie, piel, guata, vello, vision
#        print(args)
#        file.write(args[0].nombre + ", ")
#        for arg in args[1:]:
#            file.write(str(arg) + ", ")
#        file.write("\n")


# raise TypeError
personas = [Persona_con_fenotipo(args[0].nombre, args[0].apellido,
                                 args[0].genoma, args[0].caracteristicas,
                                 *args[1:])
            for args in zip(personas, alturas, ojos, pelos, pieles, narices,
                            pies, vellos, guatas, visiones)]

# parientes_grado_1 = map(determinar_grado_1, ((persona,
#  filter(lambda x: x != persona, personas)) for persona in personas))

# parientes_gradon = map(determinar_grado_n, ((persona,
# filter(lambda x: x != persona, personas)) for persona in personas))

# parientes_grado0 = map(determinar_grado0, ((persona,
# filter(lambda x: x != persona, personas)) for persona in personas))

# parientes_grado1 = map(determinar_grado1, ((persona,
# filter(lambda x: x != persona, personas)) for persona in personas))

# parientes_grado2 = map(determinar_grado2, ((persona,
# filter(lambda x: x != persona, personas)) for persona in personas))


# a = ["".join(x) for _, x in groupby("dfsd98sd8f68as7df56",
# key=str.isdigit) if _ == True]
# print(a)
# for elem in groupby("hola2chao3", key=str.isdigit):
#    print("".join(elem[1]))

# for persona in personas:
#    print(persona)
# print("TAMAÑOOOO", sys.getsizeof(personas))
