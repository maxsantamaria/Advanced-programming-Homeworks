import zlib
import os
from collections import deque
import re


class Image:
    def __init__(self, chunk_ihdr, chunk_idat, chunk_iend):
        self.header = None
        self.ihdr = chunk_ihdr
        self.idat = chunk_idat
        self.iend = chunk_iend
        self.matriz_rgb = None
        self.nombre = None
        self.comentarios = None

    @property
    def ancho(self):
        self._ancho = int.from_bytes(self.ihdr.informacion[0:4],
                                     byteorder="big")
        return self._ancho

    @property
    def alto(self):
        self._alto = int.from_bytes(self.ihdr.informacion[4:8],
                                    byteorder="big")
        return self._alto

    @property
    def bytes_archivo(self):
        self._bytes_archivo = bytearray()
        self._bytes_archivo += self.header
        self._bytes_archivo += self.ihdr.largo_informacion.\
            to_bytes(4, byteorder="big")
        self._bytes_archivo += self.ihdr.tipo.encode()
        self._bytes_archivo += self.ihdr.informacion
        self._bytes_archivo += self.ihdr.crc
        self._bytes_archivo += self.idat.largo_informacion.\
            to_bytes(4, byteorder="big")
        self._bytes_archivo += self.idat.tipo.encode()
        self._bytes_archivo += self.idat.informacion
        idat_crc = zlib.crc32(self.idat.tipo.encode() + self.idat.informacion)
        crc = idat_crc.to_bytes(4, byteorder="big")
        self._bytes_archivo += crc
        self._bytes_archivo += self.iend.largo_informacion.\
            to_bytes(4, byteorder="big")
        self._bytes_archivo += self.iend.tipo.encode()
        self._bytes_archivo += self.iend.crc
        return self._bytes_archivo

    def generar_matriz_rgb(self):
        self.matriz_rgb = bytearray(zlib.decompress(self.idat.informacion))

    def acceder_a_pixel(self, posicion):  # posicion es tupla (x, y)
        x = posicion[0]
        y = posicion[1]
        fila = (self.ancho * 3 + 1) * y
        columna = 1 + 3 * x
        posicion_en_matriz = fila + columna
        return posicion_en_matriz

    def vecinos_pixeles(self, posicion_actual):
        x = posicion_actual[0]
        y = posicion_actual[1]
        izquierda = self.acceder_a_pixel((x - 1, y))
        derecha = self.acceder_a_pixel((x + 1, y))
        arriba = self.acceder_a_pixel((x, y - 1))
        abajo = self.acceder_a_pixel((x, y + 1))
        return izquierda, derecha, arriba, abajo

    def vecinos_bytes(self, posicion_actual_matriz):
        izquierda = posicion_actual_matriz - 3
        arriba_izq = posicion_actual_matriz - (3 * self.ancho + 1) - 3
        arriba_der = posicion_actual_matriz - (3 * self.ancho + 1) + 3
        abajo_izq = posicion_actual_matriz + (3 * self.ancho + 1) - 3
        abajo_der = posicion_actual_matriz - (3 * self.ancho + 1) + 3
        if self.transformador_matriz_pixel(izquierda)[1] != \
                self.transformador_matriz_pixel(posicion_actual_matriz)[1]:
            izquierda = None
            arriba_izq = None
            abajo_izq = None
        derecha = posicion_actual_matriz + 3
        if self.transformador_matriz_pixel(derecha)[1] != \
                self.transformador_matriz_pixel(posicion_actual_matriz)[1]:
            derecha = None
            arriba_der = None
            abajo_der = None
        arriba = posicion_actual_matriz - (3 * self.ancho + 1)
        if self.transformador_matriz_pixel(arriba)[1] < 0:
            arriba = None
            arriba_izq = None
            arriba_der = None
        abajo = posicion_actual_matriz + (3 * self.ancho + 1)
        if self.transformador_matriz_pixel(abajo)[1] > self.alto - 1:
            abajo = None
            abajo_izq = None
            abajo_der = None
        return izquierda, derecha, arriba, abajo, arriba_izq, \
            arriba_der, abajo_izq, abajo_der

    def transformador_matriz_pixel(self, posicion_matriz):
        x = ((posicion_matriz % (3 * self.ancho + 1)) - 1) // 3
        y = posicion_matriz // (3 * self.ancho + 1)
        return x, y


class Chunk:
    def __init__(self, largo_informacion, tipo, informacion, crc):
        self.largo_informacion = largo_informacion
        self.tipo = tipo
        self.informacion = informacion
        self.crc = crc


class ihdr(Chunk):
    def __init__(self, largo_informacion, tipo, informacion, crc):
        super().__init__(largo_informacion, tipo, informacion, crc)


class idat(Chunk):
    def __init__(self, largo_informacion, tipo, informacion, crc):
        super().__init__(largo_informacion, tipo, informacion, crc)


class iend(Chunk):
    def __init__(self, largo_informacion, tipo, informacion, crc):
        super().__init__(largo_informacion, tipo, informacion, crc)


def separar_imagen(imagen):
    with open(os.path.join('server/image', imagen), 'rb') as file:
        todo = file.read()
        header = todo[0:8]
        body = todo[8:]
        return header, body


def leer_estructura_chunk(body):
    i = 0
    largo_idat = 0
    informacion_idat = bytearray()
    while True:
        largo_informacion = int.from_bytes(body[i:i + 4], byteorder="big")
        tipo_de_bloque = body[i + 4: i + 8].decode()
        informacion = body[i + 8: i + 8 + largo_informacion]
        crc = body[i + 8 + largo_informacion: i + 12 + largo_informacion]
        if tipo_de_bloque == "IEND":
            chunk_iend = iend(largo_informacion, tipo_de_bloque,
                              informacion, crc)
            break
        elif tipo_de_bloque == "IDAT":
            informacion_idat += informacion
            largo_idat += largo_informacion
        elif tipo_de_bloque == "IHDR":
            chunk_ihdr = ihdr(largo_informacion, tipo_de_bloque,
                              informacion, crc)
        i = i + 12 + largo_informacion
    chunk_idat = idat(largo_idat, "IDAT", informacion_idat, "")
    new_image = Image(chunk_ihdr, chunk_idat, chunk_iend)
    return new_image


def creando_nueva_imagen(image):
    total = bytearray()
    total += image.header
    total += image.ihdr.largo_informacion.to_bytes(4, byteorder="big")
    total += image.ihdr.tipo.encode()
    total += image.ihdr.informacion
    total += image.ihdr.crc
    total += image.idat.largo_informacion.to_bytes(4, byteorder="big")
    total += image.idat.tipo.encode()
    total += image.idat.informacion
    idat_crc = zlib.crc32(image.idat.tipo.encode()
                          + image.idat.informacion)
    crc = idat_crc.to_bytes(4, byteorder="big")
    total += crc
    total += image.iend.largo_informacion.to_bytes(4, byteorder="big")
    total += image.iend.tipo.encode()
    total += image.iend.crc
    with open("mickeymouse3.png", "wb") as file:
        file.write(total)


def recortar_imagen(image, v1, v2):  # v1 pto inicial arriba izquierda,
    # v2 pto final abajo derecha
    x1 = v1[0]
    y1 = v1[1]
    x2 = v2[0]
    y2 = v2[1]
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            posicion = (x, y)
            i = image.acceder_a_pixel(posicion)
            image.matriz_rgb[i: i + 3] = b"\xff\xff\xff"
    image.idat.informacion = zlib.compress(image.matriz_rgb)
    image.idat.largo_informacion = len(image.idat.informacion)
    # creando_nueva_imagen(image)
    print("Se creo una nueva imagen recortada")
    return image


def balde_azul(image, posicion, color, parent):  # posicion (x, y), color 3 B
    i = image.acceder_a_pixel(posicion)
    color_actual = image.matriz_rgb[i: i + 3]
    propagacion = deque()
    propagacion.append(i)

    while len(propagacion) > 0:
        i = propagacion.popleft()
        image.matriz_rgb[i: i + 3] = color
        izq, der, arr, aba = image.vecinos_bytes(i)[:4]
        if izq is not None and image.matriz_rgb[izq: izq + 3] == color_actual:
            if izq not in propagacion:
                propagacion.append(izq)
        if der is not None and image.matriz_rgb[der: der + 3] == color_actual:
            if der not in propagacion:
                propagacion.append(der)
        if arr is not None and image.matriz_rgb[arr: arr + 3] == color_actual:
            if arr not in propagacion:
                propagacion.append(arr)
        if aba is not None and image.matriz_rgb[aba: aba + 3] == color_actual:
            if aba not in propagacion:
                propagacion.append(aba)
    image.idat.informacion = zlib.compress(image.matriz_rgb)
    image.idat.largo_informacion = len(image.idat.informacion)
    # creando_nueva_imagen(image)
    parent.image = image
    parent.aviso.deleteLater()
    parent.actualizar_label()
    # return image


def blurry(image, parent):
    posicion = 1
    nueva_matriz = image.matriz_rgb
    pbar = parent.pbar
    while posicion < len(image.matriz_rgb):
        # print(posicion, image.transformador_matriz_pixel(posicion))
        suma_total = 0
        ponderadores = 0
        izquierda, derecha, arriba, abajo, arriba_izq, \
            arriba_der, abajo_izq, abajo_der = image.vecinos_bytes(posicion)
        for i in range(0, 3):
            if izquierda is not None:
                suma_total += image.matriz_rgb[izquierda + i] * 2
                ponderadores += 2
                if arriba_izq is not None:
                    suma_total += image.matriz_rgb[arriba_izq + i]
                    ponderadores += 1
                if abajo_izq is not None:
                    suma_total += image.matriz_rgb[abajo_izq + i]
                    ponderadores += 1
            if derecha is not None:
                suma_total += image.matriz_rgb[derecha + i] * 2
                ponderadores += 2
                if arriba_der is not None:
                    suma_total += image.matriz_rgb[arriba_der + i]
                    ponderadores += 1
                if abajo_der is not None:
                    suma_total += image.matriz_rgb[abajo_der + i]
                    ponderadores += 1
            if arriba is not None:
                suma_total += image.matriz_rgb[arriba + i] * 2
                ponderadores += 2
            if abajo is not None:
                suma_total += image.matriz_rgb[abajo + i] * 2
                ponderadores += 2
            suma_total += image.matriz_rgb[posicion] * 4
            ponderadores += 4
            nueva_matriz[posicion + i] = round(suma_total / ponderadores)

        fila_actual = image.transformador_matriz_pixel(posicion)[1]
        posicion += 3
        if fila_actual != image.transformador_matriz_pixel(posicion)[1]:
            posicion += 1
        valor = posicion / len(image.matriz_rgb) * 100
        pbar.setValue(valor)
    pbar.deleteLater()
    image.matriz_rgb = nueva_matriz
    image.idat.informacion = zlib.compress(image.matriz_rgb)
    image.idat.largo_informacion = len(image.idat.informacion)
    # creando_nueva_imagen(image)
    parent.image = image
    parent.actualizar_label()
    # return image


def format_comentarios(comentario):
    formateado = " "

    texto = re.sub('(:poop:)', '<img src=emojis/emot_02.png>', comentario[0])
    texto = re.sub('(O:\))', '<img src=emojis/emot_09.png>', texto)
    texto = re.sub('(:D)', '<img src=emojis/emot_01.png>', texto)
    texto = re.sub('(;\))', '<img src=emojis/emot_05.png>', texto)
    texto = re.sub('(8\))', '<img src=emojis/emot_04.png>', texto)
    texto = re.sub('(U\.U)', '<img src=emojis/emot_25.png>', texto)
    texto = re.sub('(:\()', '<img src=emojis/emot_07.png>', texto)
    texto = re.sub('(3:\))', '<img src=emojis/emot_06.png>', texto)
    texto = re.sub('(o\.o)', '<img src=emojis/emot_10.png>', texto)
    texto = re.sub('(:v)', '<img src=emojis/emot_03.png>', texto)

    formateado += texto
    formateado += " <b>por " + comentario[1] + "</b>"
    formateado += " | " + comentario[2] + "<br/>"
    return formateado


if __name__ == "__main__":
    header, body = separar_imagen("MickeyMouse.png")
    imagen = leer_estructura_chunk(body)
    imagen.header = header
    imagen.generar_matriz_rgb()
    print(imagen.ancho, imagen.alto)
    # creando_nueva_imagen(imagen)

    print(imagen.matriz_rgb[
          50 * (200 * 3 + 1): (50 + 1) * (222 * 3 + 1)])
    # recortar_imagen(imagen, (0, 47), (280, 556))
    # balde_azul(imagen, (220, 80))
    # blurry(imagen)
