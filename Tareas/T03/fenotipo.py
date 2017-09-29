from reader import *


def obtener_genes(personas, tag_buscado):
    genes = (genes for persona in personas
             for tag, genes in persona.caracteristicas.items()
             if tag == tag_buscado)
    return genes


def determinar_ojos(genes):
    # genes: list de genes (3 letras cada uno) de una caracteristica
    if "CCT" in genes:
        return "cafes"
    elif "AAT" in genes:
        return "azules"
    elif "CAG" in genes:
        return "verdes"


def determinar_pelo(genes):
    # genes: list de genes (3 letras cada uno) de una caracteristica
    if "GTG" in genes:
        return "negro"
    elif "AAT" in genes:
        return "rubio"
    elif "CCT" in genes:
        return "pelirrojo"


def determinar_nariz(genes):
    # genes: list de genes (3 letras cada uno) de una caracteristica
    if "TCG" in genes:
        return "aguileña"
    elif "CAG" in genes:
        return "respingada"
    elif "TAC" in genes:
        return "recta"


def determinar_altura(genes):
    # genes: list de genes (3 letras cada uno) de una caracteristica
    alta = genes.count("AGT")
    baja = genes.count("ACT")
    porcentaje = alta / (alta + baja)
    altura = 1.40 + 0.70 * porcentaje
    return altura


def determinar_pies(genes):
    grandes = genes.count("GTA")
    chicos = genes.count("CCA")
    porcentaje = grandes / (grandes + chicos)
    pies = 34 + 14 * porcentaje
    return pies


def determinar_piel(genes):
    clara = genes.count("AAT")
    oscura = genes.count("GCG")
    porcentaje = clara / (clara + oscura)
    if porcentaje >= 0.75:
        return "albino"
    elif 0.5 <= porcentaje < 0.75:
        return "blanco"
    elif 0.25 <= porcentaje < 0.5:
        return "moreno"
    elif porcentaje < 0.25:
        return "negro"


def determinar_guata(genes):
    chica = genes.count("ACT")
    grande = genes.count("AGT")
    porcentaje = chica / (chica + grande)
    if porcentaje >= 0.75:
        return "modelo"
    elif 0.5 <= porcentaje < 0.75:
        return "atleta"
    elif 0.25 <= porcentaje < 0.5:
        return "dieta"
    elif porcentaje < 0.25:
        return "guaton"


def determinar_vello(genes):
    pecho = genes.count("TGC")
    axila = genes.count("GTG")
    espalda = genes.count("CCT")
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


def determinar_vision(genes):
    daltonismo = genes.count("TTC")
    miopia = genes.count("ATT")
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

def determinar_grado_1(args): # namedtuple, list
    persona = args[0]
    resto_personas = args[1]
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


def determinar_grado_n(args):
    persona = args[0]
    resto_personas = args[1]
    parientes = [(persona, pariente) for pariente in resto_personas
                 if abs(persona.altura - pariente.altura) <= 0.7 and
                 persona.piel == pariente.piel and
                 abs(persona.pie - pariente.pie) <= 6 and
                 persona.guata == pariente.guata]
    return parientes


def determinar_grado0(args):  # namedtuple, list
    persona = args[0]
    resto_personas = args[1]
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
    parientes = [(persona, pariente) for pariente in resto_personas
                 if persona.ojo == pariente.ojo and
                 persona.pelo == pariente.pelo and
                 persona.nariz == pariente.nariz and
                 abs(persona.altura - pariente.altura) <= 20 and
                 abs(persona.pie - pariente.pie) <= 2 and
                 persona.piel == pariente.piel and
                 persona.vision == pariente.vision]
    return parientes


def determinar_grado2(args):  # namedtuple, list of namedtuples
    persona = args[0]
    resto_personas = args[1]
    parientes = [(persona, pariente) for pariente in resto_personas
                 if persona.pelo == pariente.pelo and
                 abs(persona.altura - pariente.altura) <= 50 and
                 abs(persona.pie - pariente.pie) <= 4 and
                 persona.piel == pariente.piel and
                 persona.vision == pariente.vision]
    return parientes



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
                                              "caracteristicas", "ojo", "pelo",
                                              "nariz", "altura", "pie", "piel",
                                              "guata", "vello", "vision"])

#for args in zip(personas, ojos, pelos, narices, alturas, pies, pieles,
#                guatas, vellos, visiones):
    # ojo, pelo, nariz, altura, pie, piel, guata, vello, vision
    #print(args)

personas = [Persona_con_fenotipo(args[0].nombre, args[0].apellido,
                                 args[0].genoma, args[0].caracteristicas,
                                 *args[1:])
            for args in zip(personas, ojos, pelos, narices, alturas, pies,
                            pieles, guatas, vellos, visiones)]

print("\nGrado 0")
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

#for persona in personas:  # para PRUEBAS
#    if persona.nombre == "El" or persona.nombre == "Nicolás" or persona.nombre == "Rick":
#        print(persona.nombre, persona.vision, persona.ojo, persona.pelo, persona.nariz, persona.piel, persona.pie, persona.altura)

#parientes_grado_1 = map(determinar_grado_1, (persona for persona in personas), (pariente for pariente in personas))

