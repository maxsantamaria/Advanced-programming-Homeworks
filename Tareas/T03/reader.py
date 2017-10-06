from collections import namedtuple
from itertools import groupby

def obtener_nombre(linea):
    linea = linea.strip()
    num = ""
    if linea[0].isnumeric():
        num += linea[0]
        lim_superior = int(num) + 1
        nombre = linea[1: lim_superior]
        if linea[1].isnumeric():
            num += linea[1]
            lim_superior = int(num) + 2
            nombre = linea[2: lim_superior]
    return nombre, lim_superior


def obtener_caracteristicas(line):
    caracteristicas = ("".join(x) for numero, x in
                       groupby(line, key=str.isdigit) if numero)
    # numero es un booleano que dice si el elemento es o no un numero
    return caracteristicas


def obtener_caracteristicas_rec(line):
    #lista_ids = [line[i] for i in range(len(line)) if line[i].isnumeric()
    #             and line[i + 1].isalpha()
    #             and line[i - 1].isalpha()]  # numeros 1 digito
    lista_ids = []
    def obtener_numero(linea, numero_actual):  # numeros más digitos
        letra = linea[0]
        if letra.isnumeric():
            numero_actual += letra
            obtener_numero(next(recorrer_linea), numero_actual)
        elif letra.isalpha():
            #if len(numero_actual) > 1:
            if numero_actual != "":
                lista_ids.append(numero_actual)
            obtener_numero(next(recorrer_linea), "")
        return numero_actual
    recorrer_linea = (line[i:] for i in range(1, len(line)))
    obtener_numero(line, "")
    return lista_ids


def obtener_genoma(letras):
    #genoma = "".join(letras[9 * 3:])
    #genomaa = letras[9 * 3:]
    genoma = (letras[i - 3: i] for i in range(len(letras)) if
              i % 3 == 0 and i != 0)
    return genoma


def conectar_genoma_listas(id, genoma, listas):
    subindices = listas[id]
    #genes = [genoma[i] for i in range(len(genoma)) if str(i) in subindices]
    genes = [gen for i, gen in enumerate(genoma) if str(i) in subindices]
    return genes


def conectar_genoma_listas2(id, genoma, listas):
    # genoma es un string con todas las letras
    subindices = listas[id]
    #genes = [genoma[i] for i in range(len(genoma)) if str(i) in subindices]
    genes = [genoma[i: i + 3] for i in range(0, len(genoma), 3) if str(i//3) in subindices]
    return genes