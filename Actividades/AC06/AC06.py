from collections import namedtuple
import random
from functools import reduce

# 1 Ciudades por pais
def ciudad_por_pais(nombre_pais, paises, ciudades):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param ciudades: lista de Ciudades (instancias)
    :return: generador
    '''
    pais = list(pais.sigla for pais in paises if pais.nombre == nombre_pais)
    sigla_pais = pais[0]
    generador = (ciudad for ciudad in ciudades
                 if ciudad.sigla_pais == sigla_pais)
    return generador


# 2 Personas por pais
def personas_por_pais(nombre_pais, paises, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    pais = list(pais.sigla for pais in paises if pais.nombre == nombre_pais)
    sigla_pais = pais[0]
    ciudades2 = [ciudad.nombre for ciudad in ciudades
                 if ciudad.sigla_pais == sigla_pais]
    generador = (persona for persona in personas
                 if persona.ciudad_residencia in ciudades2)
    return generador


# 3 Personas por ciudad
def personas_por_ciudad(nombre_ciudad, personas):
    '''
    filtramos a las personas por ciudad que queremos
    :param nombre_ciudad: str
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    generador = (persona for persona in personas
                 if persona.ciudad_residencia == nombre_ciudad)
    return generador


# 4 Personas con sueldo mayor a x
def personas_con_sueldo_mayor_a(personas, sueldo):
    '''
    :param personas: lista de Personas (instancias)
    :param sueldo: int
    :return: generador
    '''
    generador = (persona for persona in personas
                 if int(persona.sueldo) > sueldo)
    return generador


# 5 Personas ciudad y sexo dado
def personas_por_ciudad_sexo(nombre_ciudad, sexo, personas):
    '''
    :param nombre_ciudad: str
    :param sexo: str
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    generador = (persona for persona in personas
                 if persona.ciudad_residencia == nombre_ciudad
                 and persona.sexo == sexo)
    return generador


# 6 Personas por pais sexo y profesion
def personas_por_pais_sexo_profesion(nombre_pais, paises, sexo, profesion,
                                     ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param sexo: str
    :param profesion: str
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    personas_en_pais = personas_por_pais(nombre_pais, paises, ciudades,
                                         personas)
    generador = (persona for persona in personas_en_pais
                 if persona.sexo == sexo and
                 persona.area_de_trabajo == profesion)
    return generador


# 7 Sueldo promedio mundo
def sueldo_promedio(personas):
    '''
    :param personas: lista de Personas (lista de instancias)
    :return: promedio (int o float)
    '''

    sueldos = list(int(persona.sueldo) for persona in personas)
    sueldo_total = reduce(lambda x, y: x + y, sueldos)
    sueldo_promedio = sueldo_total / len(personas)
    return sueldo_promedio


# 8 Sueldo promedio de una ciudad x
def sueldo_ciudad(nombre_ciudad, personas):
    '''
    :param nombre_ciudad: str
    :param personas: lista de Personas (instancias)
    :return: promedio (int o float)
    '''
    personas_en_ciudad = personas_por_ciudad(nombre_ciudad, personas)
    sueldo_ciudad = sueldo_promedio(list(personas_en_ciudad))
    return sueldo_ciudad


# 9 Sueldo promedio de un pais x
def sueldo_pais(nombre_pais, paises, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: promedio (int o float)
    '''
    personas_en_pais = personas_por_pais(nombre_pais, paises, ciudades,
                                         personas)
    sueldo_pais = sueldo_promedio(list(personas_en_pais))
    return sueldo_pais

# 10 Sueldo promedio de un pais y profesion x
def sueldo_pais_profesion(nombre_pais, paises, profesion, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param profesion: str
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: promedio (int o float)
    '''
    personas_en_pais = personas_por_pais(nombre_pais, paises, ciudades,
                                         personas)
    personas_profesion = (persona for persona in personas_en_pais
                          if persona.area_de_trabajo == profesion)
    sueldo_pais_profesion = sueldo_promedio(list(personas_profesion))
    return sueldo_pais_profesion


if __name__ == '__main__':


    """Abra los archivos y guarde en listas las instancias; paises, ciudades,
    personas"""
    parser = lambda line: line.strip().split(",")

    Ciudad = namedtuple("Ciudad", ["sigla_pais", "nombre"])
    with open('Ciudades.txt', 'r', encoding='utf-8') as file1:
        ciudades = [Ciudad(*parser(linea)) for linea in file1]

    Persona = namedtuple("Persona", ["nombre", "apellido", "edad", "sexo",
                                     "ciudad_residencia", "area_de_trabajo",
                                     "sueldo"])
    with open('Informacion_personas.txt', 'r', encoding='utf-8') as file2:
        personas = [Persona(*parser(linea)) for linea in file2]

    Pais = namedtuple("Pais", ["sigla", "nombre"])
    with open("paises.txt", "r", encoding='utf-8') as file3:
        #paises_dicc = {parser(linea)[0]: parser(linea)[1] for linea in file3}
        paises = [Pais(*parser(linea)) for linea in file3]


    """NO DEBE MODIFICAR CODIGO DESDE EL PUNTO (1) AL (10).
    EN (11) y (12) DEBEN ESCRIBIR SUS RESPUESTAS RESPECTIVAS."""

    # (1) Ciudades en Chile

    ciudades_chile = ciudad_por_pais('Chile', paises, ciudades)
    count = 0
    for ciudad in ciudades_chile:
        print(ciudad.sigla_pais, ciudad.nombre)
        count += 1
        if count == 10:
            break

    # (2) Personas en Chile
    personas_chile = personas_por_pais('Chile', paises, ciudades, personas)
    count = 0
    for p in personas_chile:
        print(p.nombre, p.ciudad_residencia)
        count += 1
        if count == 10:
            break

    # (3) Personas en Osorno, Chile
    personas_stgo = personas_por_ciudad('Osorno', personas)
    for p in personas_stgo:
        print(p.nombre, p.ciudad_residencia)

    # (4) Personas en el mundo con sueldo mayor a 600
    p_sueldo_mayor_600 = personas_con_sueldo_mayor_a(personas, 600)
    count = 0
    for p in p_sueldo_mayor_600:
        print(p.nombre, p.sueldo)
        count += 1
        if count == 10:
            break

    # (5) Personas en ViñaDelMar, Chile de sexo femenino
    pxcs = personas_por_ciudad_sexo('ViñaDelMar', 'Femenino', personas)
    for p in pxcs:
        print(p.nombre, p.ciudad_residencia, p.sexo)

    # (6) Personas en Chile de sexo masculino y area Medica
    pxpsp = personas_por_pais_sexo_profesion('Chile', paises, 'Masculino',
                                             'Medica', ciudades, personas)
    for p in pxpsp:
        print(p.nombre, p.sexo, p.area_de_trabajo)

    # (7) Sueldo promedio de personas del mundo
    sueldo_mundo = sueldo_promedio(personas)
    print('Sueldo promedio: ', sueldo_mundo)

    # (8) Sueldo promedio Osorno, Chile
    sueldo_santiago = sueldo_ciudad('Osorno', personas)
    print('Sueldo Osorno: ', sueldo_santiago)

    # (9) Sueldo promedio Chile
    sueldo_chile = sueldo_pais('Chile', paises, ciudades, personas)
    print('Sueldo Chile: ', sueldo_chile)

    # (10) Sueldo promedio Chile de un estudiante
    sueldo_chile_estudiantes = \
        sueldo_pais_profesion('Chile', paises, 'Estudiante', ciudades,
                              personas)
    print('Sueldo estudiantes Chile: ', sueldo_chile_estudiantes)

    # (11) Muestre a los 10 Chilenos con mejor sueldo con un indice de orden
    # desde 0.
    sueldo_chile = list(personas_por_pais('Chile', paises, ciudades, personas))
    sueldo_chile.sort(key=lambda x: x.sueldo, reverse = True)
    #print(sueldo_chile[:10])
    mejores_sueldos = sueldo_chile[:10]
    for posicion, chileno in enumerate(mejores_sueldos):
        print("{}, {}, {}".format(posicion, chileno.nombre, chileno.sueldo))


    # (12) Se pide seleccionar 10 personas al azar y generar tuplas con sus:
    # nombres, apellidos y sueldos.
    random.shuffle(personas)  # mezclamos las posiciones de la lista
    diez_personas = list(personas)[:10]
    personas_seleccionadas = list([persona.nombre, persona.apellido,
                                   int(persona.sueldo)]
                                  for persona in diez_personas)

    zipped = zip(*personas_seleccionadas)
    zipped = list(zipped)
    print("Nombres: {}".format(zipped[0]))
    print("Apellidos: {}".format(zipped[1]))
    print("Sueldos: {}".format(zipped[2]))

