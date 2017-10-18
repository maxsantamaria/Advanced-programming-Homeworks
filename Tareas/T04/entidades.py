from abc import ABCMeta, abstractmethod
from collections import deque
import numpy
from random import triangular, random, randint, choice, expovariate
from math import e
import csv


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
        self.preferencias_snack = []  # borrar despues
        self.colas_snack = []
        self.colas_almuerzo = []
        self.ind_cola_actual = 0
        self.tiempo_comienzo_atencion = None  # va a ir aumentando debido a la espera
        self._tiempo_llegada_a_puestos = None
        self.numero_de_rechazos = 0
        self.quick = False  # True si es que come en quick devil
        # lista de puestos preferidos (mayor a menor) cuyos elementos son
        # colas (atributo de Vendedores)


    def ingresar_a_cola_snack(self, tiempo_actual):
        cola = self.colas_snack[self.ind_cola_actual]()
        cola.append(self)  # entramos al final
        self.tiempo_comienzo_atencion = tiempo_actual

    def ingresar_a_cola_almuerzo(self, tiempo_actual):
        cola = self.colas_almuerzo[self.ind_cola_actual]()
        cola.append(self)  # entramos al final
        self.tiempo_comienzo_atencion = tiempo_actual

    def cambiar_de_cola1(self):
        cola_anterior = self.colas_snack[self.ind_cola_actual]()
        cola_anterior.remove(self)
        self.numero_de_rechazos += 1
        if self.ind_cola_actual + 1 >= len(self.colas_snack):
            return False
        self.ind_cola_actual += 1
        cola_nueva = self.colas_snack[self.ind_cola_actual]()
        cola_nueva.append(self)

    def cambiar_de_cola2(self):
        cola_anterior = self.colas_almuerzo[self.ind_cola_actual]()
        self.ind_cola_actual += 1
        self.numero_de_rechazos += 1
        cola_nueva = self.colas_almuerzo[self.ind_cola_actual]()
        cola_anterior.remove(self)
        cola_nueva.append(self)

    def generar_tiempo_llegada_universidad(self, c_llegada):
        self._tiempo_llegada_universidad = triangular(0, 240, c_llegada)

    def generar_tiempo_decidir_comprar_snack(self, tiempo_actual):
        self._tiempo_decidir_comprar_snack = tiempo_actual + expovariate(0.3)

    def generar_tiempo_llegada_a_puestos(self, lambda_traslado):
        traslado = expovariate(lambda_traslado)
        if traslado > 3 * lambda_traslado:
            traslado = 3 * lambda_traslado
        self._tiempo_llegada_a_puestos = self._tiempo_decidir_comprar_snack +\
                                         traslado

    @property
    def tiempo_paciencia(self):
        self._tiempo_paciencia -= self.numero_de_rechazos * 5
        if self._tiempo_paciencia < 0:
            return 0
        return self._tiempo_paciencia


    @property
    def tiempo_llegada_universidad(self):
        return self._tiempo_llegada_universidad

    @property
    def tiempo_decidir_comprar_snack(self):
        return self._tiempo_decidir_comprar_snack

    @property
    def tiempo_llegada_a_puestos(self):
        return self._tiempo_llegada_a_puestos

    def __str__(self):
        imprimir = self.nombrecompleto
        return imprimir




class Alumno(MiembroUC):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)

    def generar_mesada(self, base_mesada):
        self.mesada = base_mesada * (1 + random() ** random()) * 20

    def generar_pesos_diarios(self):
        self.pesos_diarios = self.mesada / 20

    def generar_tiempo_paciencia(self, alpha, beta):  # VA EN ALUMNO DESPUES
        self._tiempo_paciencia = randint(alpha, beta)

    def __str__(self):
        imprimir = "ALUMNO " +self.nombrecompleto
        return imprimir



class Funcionario(MiembroUC):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)
        self.pesos_diarios = None
        self.numero_de_rechazos = 0
        self.colas_usadas = []  # se usará para no repetir la misma cola en una misma compra
        self._tiempo_paciencia = float("Inf")

    @property
    def tiempo_paciencia(self):
        return self._tiempo_paciencia

    def generar_pesos_diarios(self, valor=7000):
        self.pesos_diarios = 7000  # CAMBIAR POR VALOR

    def reset_cambios_de_cola(self):
        self.cambios_de_cola = 0

    def ingresar_a_cola_snack(self, tiempo_actual):
        cola_func = choice(list(set(self.colas_snack) - set(self.colas_usadas)))
        self.ind_cola_actual = self.colas_snack.index(cola_func)
        cola = cola_func()
        self.colas_usadas.append(cola_func)
        if len(cola) == 0:
            cola.append(self)  # entramos al final
        else:
            funcionarios_en_cola = len(list(filter(lambda x: isinstance(x, Funcionario), cola)))
            if isinstance(cola[0], Alumno):
                index = funcionarios_en_cola + 1
            elif isinstance(cola[0], Funcionario):
                index = funcionarios_en_cola
            cola.insert(index, self)
        self.tiempo_comienzo_atencion = tiempo_actual

    def cambiar_de_cola1(self):
        cola_anterior = self.colas_snack[self.ind_cola_actual]()
        cola_anterior.remove(self)
        self.numero_de_rechazos += 1
        if len(set(self.colas_snack) - set(self.colas_usadas)) == 0 or self.numero_de_rechazos == 4:
            return False
        self.ingresar_a_cola_snack(self.tiempo_comienzo_atencion)  # es instantaneo

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
        self.unidades_vendidas = 0
        self.dias_sin_ventas = 0  # dias seguidos
        self.rapidez_atencion = None
        self.stock = None
        self.fiscalizando = False  # True cuando está siendo fiscalizado
        self.permiso = None  # True cuando lo tiene, False cuando no

    def entrega_cola(self):
        def _entrega_cola():
            return self.cola
        return _entrega_cola

    def generar_rapidez_atencion(self, alpha, beta):
        self.rapidez_atencion = randint(alpha, beta)  # en minutos

    def generar_stock(self, alpha, beta):
        self.stock = randint(alpha, beta)

    def generar_permisos(self, prob_permiso):
        prob = random()
        if prob <= prob_permiso:
            self.permiso = True
        else:
            self.permiso = False

    @property
    def tiempo_atencion_primer_cliente(self):
        primer_cliente = self.cola[0]
        return primer_cliente.tiempo_comienzo_atencion + self.rapidez_atencion

    def tiempo_atencion(self, tiempo_actual):
        return tiempo_actual + self.rapidez_atencion

    def __str__(self):
        imprimir = self.nombrecompleto
        return imprimir


class Carabinero(Persona):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)
        self.personalidad = choice(["jekill", "hide"])
        self.vendedor_actual = None
        self.tiempo_inicio = 120
        self.fiscalizados = []
        self.tasa_productos_revisar = None
        self.prob_engaño = None

    def generar_tasa_productos_revisar(self, tasa_jekyll, tasa_hyde):
        if self.personalidad == "jekill":
            self.tasa_productos_revisar = tasa_jekyll
        elif self.personalidad == "hyde":
            self.tasa_productos_revisar = tasa_hyde

    def generar_prob_engaño(self, prob_jekyll, prob_hyde):
        if self.personalidad == "jekill":
            self.prob_engaño = prob_jekyll
        elif self.personalidad == "hyde":
            self.prob_engaño = prob_hyde

    def fiscalizar(self, vendedor, tiempo):
        vendedor.fiscalizando = True
        self.vendedor_actual = vendedor
        self.tiempo_inicio = tiempo
        if not vendedor.permiso:
            pass

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
        self.calorias = float(calorias)
        self.tasa_putrefaccion = float(tasa_putrefaccion)
        self.putrefaccion = 0
        self.calidad = 0

    @property
    def puesto_de_comida(self):
        if self._puesto_de_comida == "Puesto de snacks":
            return "Snack"
        elif self._puesto_de_comida == "Puesto de comida mexicana":
            return "Mexicana"
        elif self._puesto_de_comida == "Puesto de comida china":
            return "China"

    def actualizar_putrefaccion(self, tiempo_actual):
        self.putrefaccion = 1 - e ** (-tiempo_actual / self.tasa_putrefaccion)

    def actualizar_calidad(self):
        self.calidad = (self.calorias * (1 - self.putrefaccion)**4) / \
                       self.precio ** (4/5)

    def __repr__(self):
        imprimir = self.nombre + " $" + str(self.precio)\
                   + " Calidad " + str(self.calidad)
        return imprimir

def union_vendedores_compradores():
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
                comprador.preferencias_snack.append(vendedor.nombre)  # BORRAR DESPUES, SOLO PRUEBAS
            else:
                comprador.colas_almuerzo.append(vendedor.entrega_cola())

def union_vendedores_productos():
    vendedores = [persona for persona in personas
                  if isinstance(persona, Vendedor)]
    for vendedor in vendedores:
        for producto in productos:
            if vendedor.tipo_de_comida == producto.puesto_de_comida:
                vendedor.productos.append(producto)
        vendedor.productos.sort(key=lambda x: x.precio)

with open("personas.csv", newline="", encoding="utf-8") as csvfile:
    personas_reader = csv.reader(csvfile, delimiter=";")
    reader = csv.DictReader(csvfile, delimiter=";", skipinitialspace=True)
    personas = []
    #header = next(csvfile)
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
                                    row["Edad"])
        personas.append(new_person)

with open("productos.csv", newline="", encoding="utf-8") as csvfile2:
    productos_reader = csv.reader(csvfile2, delimiter=";")
    reader = csv.DictReader(csvfile2, delimiter=";", skipinitialspace=True)
    productos = []
    for row in reader:
        new_product = Producto(row["Producto"], row["Tipo"], row["Vendido en"],
                               row["Precio"], row["Calorias"],
                               row["Tasa Putrefacción"])
        productos.append(new_product)




union_vendedores_compradores()
union_vendedores_productos()



#persona = personas[0]
#cola = persona.colas_snack[0]()
#cola.append(1)
#print()
#print(personas[0].colas_snack, personas[0].preferencias)
#vendedor = (ven for ven in personas if ven.nombre == "Jurgen")
#vendedor = next(vendedor)
#print(vendedor.nombre, vendedor.cola)

