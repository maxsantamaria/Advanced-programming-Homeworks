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
    parientes = [(persona, pariente) for pariente in resto_personas
                 if abs(persona.altura - pariente.altura) <= 0.7 and
                 persona.piel == pariente.piel and
                 abs(persona.pie - pariente.pie) <= 6 and
                 determinar_diferencia_guata(persona.guata, pariente.guata)]
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
