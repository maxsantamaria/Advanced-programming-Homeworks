# from principal import *
from fenotipo import *
from math import sqrt
from functools import reduce, wraps
from itertools import count
from collections import *
from excepciones import *
from inspect import signature
from matplotlib import pyplot as plt


# Decoradores
def param_correctos(func):
    @wraps(func)  # para que no le cambie el nombre
    def _param_correctos(*args):
        cantidad_requerida = len(signature(func).parameters)
        if cantidad_requerida != len(args):
            raise NotFound
        parametros = map(parametro_correcto, args, signature(func).parameters)
        # ese map revisa que el parametro sea correcto y que este en el orden
        # correspondiente a la funcion
        if False in parametros:
            raise NotFound
        return func(*args)
    return _param_correctos


def control_error_ascendencia(func):
    @wraps(func)
    def _control_error_ascendencia(persona):
        personaa = filter(lambda x: x.nombre == persona, personas)
        pers = next(personaa)
        if pers.pelo is None or pers.vello is None or pers.nariz\
                is None or pers.piel is None or pers.pie is None \
                or pers.guata is None:
            raise GenomeError
        return func(persona)
    return _control_error_ascendencia


def parametro_correcto(parametro_entregado, parametro_funcion):
    # parametro puede ser persona, grado o caracteristica
    grados = ["-1", "0", "1", "2", "n"]
    nombres = (persona.nombre for persona in personas)
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    if parametro_funcion == "grado":
        if parametro_entregado not in grados:
            return False
    elif parametro_funcion == "persona":
        if parametro_entregado not in nombres:
            return False
    else:
        if parametro_entregado not in tags:
            return False
    return True

# Fin decoradores


def obtener_parientes(grado):
    if grado == "-1":
        parientes = map(determinar_grado_1, ((persona,
                                              filter(lambda x: x != persona,
                                                     personas))
                                             for persona in personas))
    elif grado == "0":
        parientes = map(determinar_grado0, ((persona,
                                             filter(lambda x: x != persona,
                                                    personas)) for persona
                                            in personas))  # cambiar esto
    elif grado == "1":
        parientes = map(determinar_grado1, ((persona,
                                             filter(lambda x: x != persona,
                                                    personas))
                                            for persona in personas))
    elif grado == "2":
        parientes = map(determinar_grado2, ((persona,
                                             filter(lambda x: x != persona,
                                                    personas))
                                            for persona in personas))
    elif grado == "n":
        parientes = map(determinar_grado_n, ((persona,
                                              filter(lambda x: x != persona,
                                                     personas))
                                             for persona in personas))
    parientes = (parientes for iterador in parientes for parientes in iterador)
    return parientes


@param_correctos
def pariente_de(grado, persona):
    conjunto_parientes = obtener_parientes(grado)
    if grado == "-1":
        respuesta = tuple(parientes[1].nombre for parientes in
                          conjunto_parientes if parientes[0].nombre == persona)
    elif grado == "0":
        respuesta = tuple(parientes[1].nombre for parientes in
                          conjunto_parientes if parientes[0].nombre == persona)
    elif grado == "1":
        respuesta = tuple(parientes[1].nombre for parientes in
                          conjunto_parientes if parientes[0].nombre == persona)
    elif grado == "2":
        respuesta = tuple(parientes[1].nombre for parientes in
                          conjunto_parientes if parientes[0].nombre == persona)
    elif grado == "n":
        respuesta = tuple(parientes[1].nombre for parientes in
                          conjunto_parientes if parientes[0].nombre == persona)
    return respuesta


@param_correctos
@control_error_ascendencia
def ascendencia(persona):
    ascendencias = []
    # persona = list(perse for perse in personas if perse.nombre == persona)
    # pers = persona[0]
    personaa = filter(lambda x: x.nombre == persona, personas)
    pers = next(personaa)
    if pers.pelo == "negro" and "pecho" in pers.vello \
            and pers.nariz == "recta":
        ascendencias.append("mediterranea")
    if pers.pelo == "negro" and pers.piel == "negro" and pers.pie >= 44:
        ascendencias.append("africana")
    if pers.guata == "guaton" and "espalda" in pers.vello:
        ascendencias.append("estadounidense")
    if ("AAT" in pers.caracteristicas["GTC"] and
            "AAT" in pers.caracteristicas["GGA"] and "AAT"
            in pers.caracteristicas["TCT"]):
        ascendencias.append("albina")
    return ascendencias


@param_correctos
def índice_de_tamaño(persona):
    personaa = filter(lambda x: x.nombre == persona, personas)
    persona = next(personaa)
    if not persona.altura or not persona.guata:
        raise GenomeError
    genes_tamaño_altura = persona.caracteristicas["AAG"]["AGT"]
    genes_tamaño_guata = persona.caracteristicas["TGG"]["AGT"]
    opuestos_tamaño_altura = persona.caracteristicas["AAG"]["ACT"]
    opuestos_tamaño_guata = persona.caracteristicas["TGG"]["ACT"]
    porcentaje_altura = genes_tamaño_altura / (genes_tamaño_altura +
                                               opuestos_tamaño_altura)
    porcentaje_guata = genes_tamaño_guata / (genes_tamaño_guata +
                                             opuestos_tamaño_guata)
    indice = sqrt(porcentaje_altura * porcentaje_guata)
    return indice


def contador_total(persona, otra_persona):
    contadores = (contador_por_caract(persona, otra_persona, caracteristica)
                  for caracteristica in persona.caracteristicas)
    contador_total = reduce(lambda x, y: x + y, contadores)
    return contador_total


def contador_por_caract(persona, otra_persona, caracteristica):
    genes_persona = persona.caracteristicas[caracteristica]  # Counter
    genes_otra_persona = otra_persona.caracteristicas[caracteristica]
    contador_por_gen = (min(cantidad, genes_otra_persona[tag])
                        for tag, cantidad in genes_persona.items())
    try:
        contador = reduce(lambda x, y: x + y, contador_por_gen)
    except TypeError:
        return 0
    return contador


@param_correctos
def gemelo_genético(persona):
    personaa = filter(lambda x: x.nombre == persona, personas)
    persona = next(personaa)
    control_error_grado0()
    # lista = [(otra_persona, contador_total(persona, otra_persona))
    #         for otra_persona in personas if otra_persona != persona]
    # lista es una lista de tuplas con (persona, contador genes parecidos)
    # lista.sort(key=lambda x: x[1], reverse = True)
    lista = ((otra_persona, contador_total(persona, otra_persona))
             for otra_persona in personas if otra_persona != persona)
    lista = sorted(lista, key=lambda x: x[1], reverse=True)
    gemelo = lista[0][0]  # persona
    nombre_gemelo = gemelo.nombre
    return nombre_gemelo


@param_correctos
def valor_característica(tag_identificador, persona):
    personaa = filter(lambda x: x.nombre == persona, personas)
    persona = next(personaa)
    caracteristicas = (persona.altura, persona.ojo, persona.pelo, persona.piel,
                       persona.nariz, persona.pie, persona.vello,
                       persona.guata, persona.vision)
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    indice = tags.index(tag_identificador)
    if caracteristicas[indice] is None:
        raise GenomeError
    return caracteristicas[indice]


@param_correctos
def min2(tag_caracteristica):
    if tag_caracteristica == "GTC" or tag_caracteristica == "GGA" \
            or tag_caracteristica == "TCT" or tag_caracteristica == "GTA":
        menos_frecuente = caso1(tag_caracteristica, "min")
        return menos_frecuente
    elif tag_caracteristica == "AAG" or tag_caracteristica == "CTC":
        menos_frecuente = caso2(tag_caracteristica, "min")
        return menos_frecuente
    else:
        print("Esta caracteristica no es valida para esta consulta")
        raise NotFound


@param_correctos
def max2(tag_caracteristica):
    if tag_caracteristica == "GTC" or tag_caracteristica == "GGA" \
            or tag_caracteristica == "TCT" or tag_caracteristica == "GTA":
        menos_frecuente = caso1(tag_caracteristica, "max")
        return menos_frecuente
    elif tag_caracteristica == "AAG" or tag_caracteristica == "CTC":
        menos_frecuente = caso2(tag_caracteristica, "max")
        return menos_frecuente
    else:
        print("Esta caracteristica no es valida para esta consulta")
        raise NotFound


def caso1(tag_caracteristica, tipo):
    # tipo es un string que dice si buscamos el maximo o el minimo
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    indice = tags.index(tag_caracteristica) + 4
    frecuencias_particular = [persona[indice] for persona in personas]
    if None in frecuencias_particular:
        raise GenomeError
    frecuencias_sistema = Counter(frecuencias_particular)
    frecuencias_sistema = ((fenotipo, cantidad) for fenotipo, cantidad in
                           frecuencias_sistema.items())
    frecuencias_sistema = sorted(frecuencias_sistema, key=lambda x: x[1])
    if tipo == "min":
        return frecuencias_sistema[0][0]
    elif tipo == "max":
        return frecuencias_sistema[-1][0]


def caso2(tag_caracteristica, tipo):
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    indice = tags.index(tag_caracteristica) + 4
    frecuencias_particular = [persona[indice] for persona in personas]
    if None in frecuencias_particular:
        raise GenomeError
    if tipo == "min":
        return min(frecuencias_particular)
    elif tipo == "max":
        return max(frecuencias_particular)


@param_correctos
def prom(tag_caracteristica):
    if tag_caracteristica == "AAG" or tag_caracteristica == "CTC":
        tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
        indice = tags.index(tag_caracteristica) + 4
        frecuencias_particular = [persona[indice] for persona in personas]
        if None in frecuencias_particular:
            raise GenomeError
        suma = reduce(lambda x, y: x + y, frecuencias_particular)
        total = len(personas)
        promedio = suma / total
        return promedio
    else:
        raise NotFound


def visualizar(tipo):
    if tipo == "ojos":
        bubble_chart_ojos()
    elif tipo == "pelo":
        bubble_chart_pelo()
    else:
        raise NotFound
    return "BubbleChart"


def bubble_chart_ojos():
    colores = (persona.ojo for persona in personas)
    contador = Counter(colores)
    if None in contador.keys():
        raise GenomeError
    colores = [color for color in contador.keys()]
    transformador_colores = {"azules": "b", "verdes": "g",
                             "cafes": "tab:brown"}
    cantidades = [amount * 10 for amount in contador.values()]
    promedios_alturas = list(map(promedio_bubble, colores,
                                 ("ojos" for i in range(len(colores))),
                                 ("altura" for i in range(len(colores)))))
    promedios_pies = list(map(promedio_bubble, colores,
                              ("ojos" for i in range(len(colores))),
                              ("pies" for i in range(len(colores)))))
    colors = [transformador_colores[color] for color in colores]
    plt.scatter(promedios_pies, promedios_alturas, s=cantidades, c=colors)
    plt.xlabel("Promedio pies [talla]")
    plt.ylabel("Promedio alturas [cm]")
    plt.show()


def bubble_chart_pelo():
    colores = (persona.pelo for persona in personas)
    contador = Counter(colores)
    if None in contador.keys():
        raise GenomeError
    colores = [color for color in contador.keys()]
    transformador_colores = {"negro": "k", "rubio": "y",
                             "pelirrojo": "r"}
    cantidades = [amount * 10 for amount in contador.values()]
    promedios_alturas = list(map(promedio_bubble, colores,
                                 ("pelo" for i in range(len(colores))),
                                 ("altura" for i in range(len(colores)))))
    promedios_pies = list(map(promedio_bubble, colores,
                              ("pelo" for i in range(len(colores))),
                              ("pies" for i in range(len(colores)))))
    colors = [transformador_colores[color] for color in colores]
    plt.scatter(promedios_pies, promedios_alturas, s=cantidades, c=colors)
    plt.xlabel("Promedio pies [talla]")
    plt.ylabel("Promedio alturas [cm]")
    plt.show()


def promedio_bubble(color, caract1, caract2):
    if caract1 == "ojos":
        if caract2 == "altura":
            lista = [persona.altura for persona in personas
                     if persona.ojo == color]
        elif caract2 == "pies":
            lista = [persona.pie for persona in personas
                     if persona.ojo == color]
    elif caract1 == "pelo":
        if caract2 == "altura":
            lista = [persona.altura for persona in personas
                     if persona.pelo == color]
        elif caract2 == "pies":
            lista = [persona.pie for persona in personas
                     if persona.pelo == color]
    if None in lista:
        raise GenomeError
    suma = reduce(lambda x, y: x + y, lista)
    return suma/len(lista)


def num_consultas():
    # se usará en main para llevar el conteo de las consultas
    for i in count(1):
        yield i


numeros = num_consultas()

lista_consultas = [ascendencia, índice_de_tamaño, pariente_de, gemelo_genético,
                   valor_característica, min2, max2, prom, visualizar]
for persona in personas:
    if persona.nombre == "Jesús De Nazaret" or persona.nombre == "Gabriel Lyon" or persona.nombre == "Germán Contreras":
        print(persona.nombre, persona.altura, persona.pelo, persona.piel, persona.pie, persona.vision)