from abc import ABCMeta, abstractmethod
from collections import deque
import numpy
from random import triangular, random, randint, choice, expovariate, uniform,\
    normalvariate
from math import e
import csv
from datetime import datetime, timedelta


class Persona(metaclass=ABCMeta):
    def __init__(self, nombre, apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.nombrecompleto = nombre + " " + apellido


class MiembroUC(Persona):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)
        self.mesada = None
        self.pesos_diarios = None
        self.preferencias = []
        self.colas_snack = []
        self.colas_almuerzo = []
        self.ind_cola_actual = 0
        self.ind_cola_actual2 = 0
        self._tiempo_decidir_comprar_snack = None
        self._tiempo_decidir_almorzar = None
        self.tiempo_comienzo_atencion = None  # va a ir aumentando por espera
        self._tiempo_llegada_a_puestos = None
        self._tiempo_llegada_a_puestos2 = None
        self.numero_de_rechazos = 0
        self.quick = False  # True si es que come en quick devil
        self.almuerza = False  # True si almuerza ese dia
        self.distribucion_almuerzo = None  # 60, 120, 180
        self.comprando = False
        # lista de puestos preferidos (mayor a menor) cuyos elementos son
        # colas (atributo de Vendedores)

    def generar_tiempo_llegada_universidad(self, c_llegada):  # Descriptivo
        self._tiempo_llegada_universidad = triangular(0, 240, c_llegada)

    def generar_tiempo_decidir_comprar_snack(self, tiempo_actual):
        """
        Se ejecuta al llegar a la universidad. Servía para la versión anterior
        del enunciado donde se podía ir más de 1 vez a comprar un snack
        :param tiempo_actual: float
        :return:
        """
        self._tiempo_decidir_comprar_snack = tiempo_actual + expovariate(0.3)

    def generar_tiempo_decidir_comprar_snack2(self, tiempo_llegada):
        # Descriptivo
        self._tiempo_decidir_comprar_snack = uniform(tiempo_llegada, 240)

    def generar_tiempo_decidir_almorzar(self):
        """
        Genera a partir de su horario asignado (12:00, 13:00, 14:00), la hora
        en la que quiere comer ese dia
        :return:
        """
        tiempo = normalvariate(self.distribucion_almuerzo + 10, 10)
        self.tiempo_decidir_almorzar = tiempo

    def generar_tiempo_llegada_a_puestos(self, lambda_traslado):
        """
        Le agrega al tiempo de decidir ir a comer un snack,
        el tiempo de traslado hasta los puestos de comida. Tiene un valor
        máximo dado por 3 * 1 / lambda
        :param lambda_traslado: Float
        :return:
        """
        lambda_traslado = float(lambda_traslado)
        traslado = expovariate(lambda_traslado)
        if traslado > 3 * 1 / lambda_traslado:
            traslado = 3 / lambda_traslado
        self._tiempo_llegada_a_puestos = self._tiempo_decidir_comprar_snack + \
            traslado

    def generar_tiempo_llegada_a_puestos2(self, lambda_traslado):
        """
        Lo mismo que arriba pero para almorzar
        """
        lambda_traslado = float(lambda_traslado)
        traslado = expovariate(lambda_traslado)
        if traslado > 3 * 1 / lambda_traslado:
            traslado = 3 / lambda_traslado
        self._tiempo_llegada_a_puestos2 = self.tiempo_decidir_almorzar + \
            traslado

    @property
    def tiempo_llegada_universidad(self):  # Descriptivo
        return self._tiempo_llegada_universidad

    @property
    def tiempo_decidir_comprar_snack(self):  # Descriptivo
        return self._tiempo_decidir_comprar_snack

    @property
    def tiempo_decidir_almorzar(self):  # Descriptivo
        return self._tiempo_decidir_almorzar

    @tiempo_decidir_almorzar.setter
    def tiempo_decidir_almorzar(self, value):
        """
        Recibe el tiempo en el que se quiere ir a almorzar y lo compara con
        la hora de llegada a la universidad. Si es que quiere ir a comer y aun
        no ha llegado, entonces significa que no almuerza en la universidad
        ese día.
        :param value: float
        :return:
        """
        if value < self.tiempo_llegada_universidad:
            self._tiempo_decidir_almorzar = float("Inf")  # NO ALMUERZA ESE DIA
        elif value < self.distribucion_almuerzo - 60:
            self._tiempo_decidir_almorzar = self.distribucion_almuerzo - 60
        elif value > self.distribucion_almuerzo + 120:
            self._tiempo_decidir_almorzar = self.distribucion_almuerzo + 120
        else:
            self._tiempo_decidir_almorzar = value

    @property
    def tiempo_llegada_a_puestos(self):  # Descriptivo
        return self._tiempo_llegada_a_puestos

    def __str__(self):
        imprimir = self.nombrecompleto
        return imprimir


class Alumno(MiembroUC):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)

    def generar_mesada(self, base_mesada):
        """
        Con la fórmula dada, genera el dinero que tendrá en el mes
        :param base_mesada: float
        :return:
        """
        self.mesada = base_mesada * (1 + random() ** random()) * 20

    def generar_pesos_diarios(self):  # Descriptivo
        self.pesos_diarios = self.mesada / 20

    def generar_tiempo_paciencia(self, alpha, beta):  # Descriptivo
        self._tiempo_paciencia = randint(alpha, beta)

    @property
    def tiempo_paciencia(self):
        """
        El tiempo de paciencia disminuye en 5 minutos por cada rechazo
        """
        self._tiempo_paciencia -= self.numero_de_rechazos * 5
        if self._tiempo_paciencia < 0:
            return 0
        return self._tiempo_paciencia

    def ingresar_a_cola_snack(self, tiempo_actual):
        """
        Accede al primer atributo cola de un Vendedor de sus preferencias e
        ingresa en ella al final. Actualiza el tiempo de comienzo atención
        (no necesariamente el final).
        :param tiempo_actual: Float (minutos)
        :return:
        """
        cola = self.colas_snack[self.ind_cola_actual]()
        cola.append(self)  # entramos al final
        self.tiempo_comienzo_atencion = tiempo_actual

    def ingresar_a_cola_almuerzo(self, tiempo_actual):
        """
        Lo mismo que la de arriba pero para la cola de almuerzo
        :param tiempo_actual: Float (minutos)
        :return:
        """
        cola = self.colas_almuerzo[self.ind_cola_actual2]()
        cola.append(self)  # entramos al final
        self.tiempo_comienzo_atencion = tiempo_actual

    def cambiar_de_cola1(self):
        """
        Abandona la cola en la que estaba e ingresa a la siguiente del orden.
        Se modifica el índice actual que indica la posición en sus preferencias
        :return: False si no se puede cambiar (llegó al final de las
        preferencias. None si es que se pudo cambiar.
        """
        cola_anterior = self.colas_snack[self.ind_cola_actual]()
        cola_anterior.remove(self)
        # self.numero_de_rechazos += 1
        if self.ind_cola_actual + 1 >= len(self.colas_snack):
            return False
        self.ind_cola_actual += 1
        cola_nueva = self.colas_snack[self.ind_cola_actual]()
        cola_nueva.append(self)

    def cambiar_de_cola2(self):
        """
        Lo mismo que la anterior pero para colas de almuerzo
        """
        cola_anterior = self.colas_almuerzo[self.ind_cola_actual2]()
        cola_anterior.remove(self)
        # self.numero_de_rechazos += 1
        if self.ind_cola_actual2 + 1 >= len(self.colas_almuerzo):
            return False
        self.ind_cola_actual2 += 1
        cola_nueva = self.colas_almuerzo[self.ind_cola_actual2]()
        cola_nueva.append(self)

    def __str__(self):
        imprimir = "ALUMNO " + self.nombrecompleto
        return imprimir


class Funcionario(MiembroUC):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)
        self.numero_de_cambios = 0  # al tercero se va a Quick Devil
        self.colas_usadas = []
        # se usará para no repetir la misma cola en una misma compra
        self._tiempo_paciencia = float("Inf")
        self.vendedores_dia_anterior_snack = []
        self.vendedores_dia_anterior_almuerzo = []
        self.cola_ignorada_snack = None
        self.cola_ignorada_almuerzo = None

    @property
    def tiempo_paciencia(self):  # Descriptivo
        return self._tiempo_paciencia

    def generar_pesos_diarios(self, valor):  # Descriptivo
        self.pesos_diarios = float(valor)  # CAMBIAR POR VALOR

    def reset_cambios_de_cola(self):  # Descriptivo
        self.cambios_de_cola = 0

    def ingresar_a_cola_snack(self, tiempo_actual):
        """
        Elige una de sus preferencias al azar (que no haya sido usada) e
        ingresa en ella. Si no hay nadie, entra como el primero, si hay
        alguien, entra detrás del último funcionario que haya o si no hay
        funcionarios, entra detrás del que están atendiendo.
        :param tiempo_actual: float (minutos)
        :return:
        """
        cola_func = choice(list(set(self.colas_snack) -
                                set(self.colas_usadas)))
        self.ind_cola_actual = self.colas_snack.index(cola_func)
        self.colas_usadas.append(cola_func)
        cola = cola_func()
        if len(cola) == 0:
            cola.append(self)  # entramos al final
        else:
            funcionarios_en_cola = len(list(filter(lambda x:
                                                   isinstance(x, Funcionario),
                                                   cola)))
            if isinstance(cola[0], Alumno):
                index = funcionarios_en_cola + 1
            elif isinstance(cola[0], Funcionario):
                index = funcionarios_en_cola
            cola.insert(index, self)
        self.tiempo_comienzo_atencion = tiempo_actual

    def ingresar_a_cola_almuerzo(self, tiempo_actual):
        """
        Lo mismo que la anterior pero para colas de almuerzo
        :param tiempo_actual: float (minutos)
        :return:
        """
        cola_func = choice(
            list(set(self.colas_almuerzo) - set(self.colas_usadas)))
        self.ind_cola_actual2 = self.colas_almuerzo.index(cola_func)
        self.colas_usadas.append(cola_func)
        cola = cola_func()
        if len(cola) == 0:
            cola.append(self)  # entramos al final
        else:
            funcionarios_en_cola = len(
                list(filter(lambda x: isinstance(x, Funcionario), cola)))
            if isinstance(cola[0], Alumno):
                index = funcionarios_en_cola + 1
            elif isinstance(cola[0], Funcionario):
                index = funcionarios_en_cola
            cola.insert(index, self)
        self.tiempo_comienzo_atencion = tiempo_actual

    def cambiar_de_cola1(self):
        """
        Se cambia de cola de snack abandonando la que estaba e ingresando a la
        siguiente. Antes de ingresar a la siguiente hace un control para ver
        si es posible ingresar a otra o si ya se cambió 3 veces (que es es el
        máximo)
        :return: False cuando no se puede cambiar de cola, None si es que puede
        """
        cola_anterior = self.colas_snack[self.ind_cola_actual]()
        cola_anterior.remove(self)
        self.numero_de_cambios += 1
        if len(set(self.colas_snack) - set(self.colas_usadas)) == 0 or \
                self.numero_de_rechazos == 4:
            return False
        self.ingresar_a_cola_snack(self.tiempo_comienzo_atencion)
        # es instantaneo

    def cambiar_de_cola2(self):
        """
        Lo mismo que la anterior pero para colas de almuerzo
        :return:
        """
        cola_anterior = self.colas_almuerzo[self.ind_cola_actual2]()
        cola_anterior.remove(self)
        # self.numero_de_rechazos += 1
        self.numero_de_cambios += 1
        if len(set(self.colas_almuerzo) - set(self.colas_usadas)) == 0 or \
                self.numero_de_rechazos == 4:
            return False
        self.ingresar_a_cola_almuerzo(self.tiempo_comienzo_atencion)
        # es instantaneo

    def __str__(self):
        imprimir = "FUNCIONARIO " + self.nombrecompleto
        return imprimir


class Vendedor(Persona):
    def __init__(self, nombre, apellido, edad, tipo_de_comida):
        super().__init__(nombre, apellido, edad)
        self.tipo_de_comida = tipo_de_comida
        self.productos = []  # lista de Producto
        self.cola = deque()
        self.contador_stock_out = 0  # cuenta cantidad de veces sin stock
        self.contador_sin_ventas = {}  # key = nombre, value = dias que no
        # se vendió, se reinicia al mes
        self.contador_sin_ventas2 = 0
        self.unidades_vendidas = {}  # key = nombre, value = unid. vendidas,
        self.unidades_vendidas2 = 0  # stock general
        # se reinicia al dia
        self.dias_sin_ventas = 0  # dias seguidos
        self.rapidez_atencion = None
        self.stock = None
        self.fiscalizando = False  # True cuando está siendo fiscalizado
        self.ausente = False  # cuando se escapa
        self.confiscado = False
        self.dias_ausente = 0  # dice cuantos dias le quedan de ausente
        self.instalado = False
        self._tiempo_instalacion = None
        self.permiso = None  # True cuando lo tiene, False cuando no
        self.enfermados = 0  # contador

    def entrega_cola(self):
        """
        Decorador que entrega el atributo cola. Se usará para que los Miembros
        UC tengan acceso a las colas y a modificarlas, pero a nada más de
        los vendedores y así evitar modelamiento circular.
        """
        def _entrega_cola():
            return self.cola
        return _entrega_cola

    def generar_rapidez_atencion(self, alpha, beta):  # Descriptivo
        self.rapidez_atencion = randint(alpha, beta)  # en minutos

    def generar_stock(self, alpha, beta):  # Descriptivo
        self.stock = randint(alpha, beta)

    def generar_permisos(self, prob_permiso):
        """
        Recibe una probabilidad de permiso y calcula con random si es que este
        vendedor tiene el permiso o no
        :param prob_permiso: float
        :return:
        """
        prob = random()
        if prob <= prob_permiso:
            self.permiso = True
        else:
            self.permiso = False

    def generar_tiempo_instalacion(self):  # Descriptivo
        self.tiempo_instalacion = normalvariate(0, 30)  # 0 = 11:00

    def promedio_precios_productos(self):  # Descriptivo
        promedio = sum([prod.precio for prod in self.productos]) / \
                   len(self.productos)
        return promedio

    @property
    def tiempo_atencion_primer_cliente(self):
        """
        Entrega el tiempo en el que termina de atender al primero de la cola
        :return: float
        """
        primer_cliente = self.cola[0]
        return primer_cliente.tiempo_comienzo_atencion + self.rapidez_atencion

    def tiempo_atencion(self, tiempo_actual):  # Descriptivo
        return tiempo_actual + self.rapidez_atencion

    @property
    def tiempo_instalacion(self):  # Descriptivo
        return self._tiempo_instalacion

    @tiempo_instalacion.setter
    def tiempo_instalacion(self, normalvar):
        """
        Recibe el valor del tiempo en el que se instaló y si es menor a las
        11:00, significa que cuando comienza la simulación del día, ya está
        instalado (no sería un evento)
        :param normalvar:
        :return:
        """
        if normalvar < 0:
            self.instalado = True
            self._tiempo_instalacion = 0
        else:
            self._tiempo_instalacion = normalvar

    def __str__(self):
        imprimir = self.nombrecompleto
        return imprimir


class Carabinero(Persona):
    def __init__(self, nombre, apellido, edad, personalidad):
        super().__init__(nombre, apellido, edad)
        self.personalidad = personalidad
        self.vendedor_actual = None
        self.tiempo_inicio = 120
        self.fiscalizados = []
        self.tasa_productos_revisar = None
        self.prob_engaño = None
        self.engaños = 0
        self.cantidad_confiscada = []

    def generar_tasa_productos_revisar(self, tasa_jekyll, tasa_hyde):
        # Descriptivo, depende de la personalidad
        if self.personalidad == "jekill":
            self.tasa_productos_revisar = tasa_jekyll
        elif self.personalidad == "hyde":
            self.tasa_productos_revisar = tasa_hyde

    def generar_prob_engaño(self, prob_jekyll, prob_hyde):
        # Descriptivo, depende de la personalidad
        if self.personalidad == "jekill":
            self.prob_engaño = prob_jekyll
        elif self.personalidad == "hyde":
            self.prob_engaño = prob_hyde

    def fiscalizar(self, vendedor, tiempo, calor_intenso):
        """
        Primero indica que está fiscalizando a tal vendedor, para limitarlo
        de que venda durante el periodo. Luego ve si tiene permiso. Si no lo
        tiene y no logró engañarlo, el vendedor se ausenta. Si lo tiene o lo
        engaña, se revisan los productos. Si encuentra alguno en mal estado
        confisca su stock.
        :param vendedor: class Vendedor
        :param tiempo: float
        :param calor_intenso: boolean
        :return:
        """
        vendedor.fiscalizando = True
        self.vendedor_actual = vendedor
        p = random()
        if not vendedor.permiso and p > self.prob_engaño:
            # no lo engaño
            # print("Te pillamos po compadre", vendedor)
            vendedor.ausente = True
        else:
            # print("Se revisarán los productos de", vendedor)
            cantidad_a_revisar = round(self.tasa_productos_revisar *
                                       len(vendedor.productos))
            if cantidad_a_revisar < 1:
                cantidad_a_revisar = 1
            aux = vendedor.productos
            for _ in range(cantidad_a_revisar):
                product = choice(aux)
                product.actualizar_putrefaccion(tiempo, calor_intenso)
                if product.putrefaccion > 0.9:  # esta descompuesto
                    vendedor.confiscado = True
                    precio = vendedor.promedio_precios_productos()
                    self.cantidad_confiscada.append(precio * vendedor.stock)
                    # print("Se encontró un producto en mal estado", product,
                    #      ". Se confisco:", precio * vendedor.stock)
                    vendedor.stock = 0
                    break
        if not vendedor.permiso and p <= self.prob_engaño:
            # lo engaño
            self.engaños += 1

    def __str__(self):
        imprimir = self.nombrecompleto + " " + self.personalidad
        return imprimir


class Producto:
    def __init__(self, nombre, tipo, puesto_de_comida, precio, calorias,
                 tasa_putrefaccion):
        self.nombre = nombre
        self.tipo = tipo  # fondo o snack
        self._puesto_de_comida = puesto_de_comida
        self.precio = float(precio)
        self.precio_minimo = 0.01 * self.precio
        self.calorias = float(calorias)
        self.tasa_putrefaccion = float(tasa_putrefaccion)
        self._putrefaccion = 0
        self.calidad = 0

    @property
    def puesto_de_comida(self):
        """
        Se usa para conectar el puesto de comida donde se venderá con el
        tipo de comida del vendedor
        """
        if self._puesto_de_comida == "Puesto de snacks":
            return "Snack"
        elif self._puesto_de_comida == "Puesto de comida mexicana":
            return "Mexicana"
        elif self._puesto_de_comida == "Puesto de comida china":
            return "China"

    def actualizar_putrefaccion(self, tiempo_actual, calor_intenso):
        """
        Actualiza la putrefacción según la fórmula y le genera el cambio
        dependiendo si es un dia caluroso o no
        :param tiempo_actual: float
        :param calor_intenso: boolean
        :return:
        """
        self.putrefaccion = 1 - e ** (-tiempo_actual / self.tasa_putrefaccion)
        if calor_intenso:
            self.putrefaccion = self.putrefaccion * 2

    def actualizar_calidad(self, frio_intenso):
        """

        :param frio_intenso:
        :return:
        """
        self.calidad = (self.calorias * (1 - self.putrefaccion)**4) / \
            self.precio ** (4/5)
        if frio_intenso:
            self.calidad = self.calidad / 2

    @property
    def putrefaccion(self):  # Descriptivo
        return self._putrefaccion

    @putrefaccion.setter
    def putrefaccion(self, value):
        """
        No permite que la putrefaccion sea mayor a 1
        """
        if value > 1:
            self._putrefaccion = 1
        else:
            self._putrefaccion = value

    def __repr__(self):
        imprimir = self.nombre + " $" + str(self.precio)\
                   + " Calidad " + str(self.calidad)
        return imprimir


class QuickDevil:
    def __init__(self):
        self.snacks = []
        self.almuerzos = []
        self.ventas = 0


def union_vendedores_compradores(personas):
    """
    Dependiendo de las preferencias de los miembrosUC, les entrega el atributo
    cola de los vendedores para unirlos. Se entrega mediante el decorador
    explicado más arriba. Se separa en preferencias para snack y almuerzo
    :param personas: Lista de Personas
    :return:
    """
    miembros_uc = [persona for persona in personas
                   if isinstance(persona, MiembroUC)]
    vendedores = [persona for persona in personas
                  if isinstance(persona, Vendedor)]
    for comprador in miembros_uc:
        preferencias = [vendedor for nombre in comprador.preferencias
                        for vendedor in vendedores if
                        vendedor.nombrecompleto == nombre]
        for vendedor in preferencias:
            if vendedor.tipo_de_comida == "Snack":
                comprador.colas_snack.append(vendedor.entrega_cola())
            else:
                comprador.colas_almuerzo.append(vendedor.entrega_cola())


def union_vendedores_productos(personas, productos, quickdevil):
    """
    A cada vendedor se le asigna una lista de productos que son los que
    vende. Al quickdevil se le dan todos los productos.
    :param personas: Lista de Personas
    :param productos: Lista de Productos
    :param quickdevil: Objeto Quickdevil
    :return:
    """
    vendedores = [persona for persona in personas
                  if isinstance(persona, Vendedor)]
    for vendedor in vendedores:
        for producto in productos:
            if vendedor.tipo_de_comida == producto.puesto_de_comida:
                vendedor.contador_sin_ventas[producto.nombre] = 0
                vendedor.unidades_vendidas[producto.nombre] = 0
                vendedor.productos.append(producto)
        vendedor.productos.sort(key=lambda x: x.precio)
    for producto in productos:
        if producto.puesto_de_comida != "Snack":
            quickdevil.snacks.append(producto)
        else:
            quickdevil.almuerzos.append(producto)
    quickdevil.snacks.sort(key=lambda x: x.precio)
    quickdevil.almuerzos.sort(key=lambda x: x.precio)


def poblar_personas():
    """
    Abre el archivo personas y genera las instancias para guardarlas en la
    lista personas
    :return: Lista de Personas
    """
    with open("personas.csv", newline="", encoding="utf-8") as csvfile:
        # personas_reader = csv.reader(csvfile, delimiter=";")
        reader = csv.DictReader(csvfile, delimiter=";", skipinitialspace=True)
        personas = []
        for row in reader:
            if row["Entidad"] == "Alumno":
                new_person = Alumno(row["Nombre"].strip(),
                                    row["Apellido"].strip(),
                                    row["Edad"].strip())
                lista = row["Vendedores de Preferencia"].strip().split(" - ")
                new_person.preferencias = lista
            elif row["Entidad"] == "Funcionario":
                new_person = Funcionario(row["Nombre"],
                                         row["Apellido"],
                                         row["Edad"])
                lista = row["Vendedores de Preferencia"].strip().split(" - ")
                new_person.preferencias = lista
            elif row["Entidad"] == "Vendedor":
                new_person = Vendedor(row["Nombre"],
                                      row["Apellido"],
                                      row["Edad"],
                                      row["Tipo Comida"].strip())
            elif row["Entidad"] == "Carabinero":
                new_person = Carabinero(row["Nombre"],
                                        row["Apellido"],
                                        row["Edad"],
                                        row["Personalidad"].strip())
            personas.append(new_person)
        return personas


def poblar_productos():
    """
    Abre el archivo de productos y genera las instancias con sus informaciones
    :return: Lista de Productos
    """
    with open("productos.csv", newline="", encoding="utf-8") as csvfile2:
        productos_reader = csv.reader(csvfile2, delimiter=";")
        reader = csv.DictReader(csvfile2, delimiter=";", skipinitialspace=True)
        productos = []
        for row in reader:
            new_product = Producto(row["Producto"], row["Tipo"],
                                   row["Vendido en"],
                                   row["Precio"], row["Calorias"],
                                   row["Tasa Putrefacción"])
            productos.append(new_product)
        return productos
