from pi import pi
from functools import reduce
import time


def algoritmo_1(bad_array):
    array_arreglado = bytearray()
    for i in range(0, len(bad_array), 3):
        tres_numeros = bad_array[i: i + 3]
        multiplicacion = reduce(lambda x, y: x * y, tres_numeros)
        resultado = 255 - multiplicacion
        array_arreglado.extend([resultado])
    return array_arreglado


def algoritmo_2(bad_array):
    array_arreglado = bytearray()
    for i in range(0, len(bad_array), 3):
        tres_numeros = bad_array[i: i + 3]
        byte_original = ""
        for numero in tres_numeros:
            numero_tres_digitos = "{:0>3}".format(str(numero))
            numero_invertido = int(str(numero_tres_digitos)[::-1])
            if numero_invertido > 255:
                numero_invertido = numero

            byte_original += str(numero_invertido)[0]
        array_arreglado.extend([int(byte_original)])
    return array_arreglado


transformador = {"1": 12000,
                 "2": 11235,
                 "3": 6000,
                 "4": 15000,
                 "5": 12345,
                 "6": 9999,
                 "7": 22233,
                 "8": 13131,
                 "9": 24000}

algoritmos = [algoritmo_1, algoritmo_2]


with open("potato.potato", "rb") as file1:
    with open("herp.derp", "rb") as file2:
        array_final = bytearray()
        potato = True
        for numero in pi:
            if numero == "0":
                algoritmos.reverse()
            else:
                limite = transformador[numero]
                array_malo = bytearray()
                if potato:
                    data_potato = file1.read(limite)
                    for elem in data_potato:
                        array_malo.extend([int(elem)])
                    if int(numero) % 2 == 0:
                        arreglado = algoritmos[0](array_malo)
                    else:
                        arreglado = algoritmos[1](array_malo)
                    potato = False
                else:
                    data_herp = file2.read(limite)
                    for elem in data_herp:
                        array_malo.extend([int(elem)])
                    if int(numero) % 2 == 0:
                        arreglado = algoritmos[0](array_malo)
                    else:
                        arreglado = algoritmos[1](array_malo)
                    potato = True
                array_final += arreglado


with open("video.mp4", "wb") as resultado:
    largo_total = len(array_final)
    print(largo_total, "LARGO")
    print("|{0: ^15s}|{1: ^15s}|{2: ^16s}|{3: ^16s}|".format("Total",
                                                             "Procesado",
                                                             "Sin procesar",
                                                             "Deltatime"))
    procesado = 0
    tiempo_inicio = time.time()
    for a in range(0, len(array_final), 2024):
        procesado += 2024
        if procesado > largo_total:
            procesado = largo_total
        sin_procesar = largo_total - procesado
        resultado.write(array_final[a: a + 2024])
        tiempo_final = time.time()
        delta = tiempo_final - tiempo_inicio
        print("|{0: ^15d}|{1: ^15d}|{2: ^16d}|{3: ^16.6f}|".
              format(largo_total, procesado, sin_procesar, delta))
