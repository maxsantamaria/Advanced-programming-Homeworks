from abc import ABCMeta, abstractmethod
from collections import deque
import numpy
from random import triangular, random, randint, choice, expovariate


class Persona(metaclass=ABCMeta):
    def __init__(self, nombre, apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad


class MiembroUC(Persona):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)
        self.mesada = None
        self.pesos_diarios = None
        self.preferencias = []
        # lista de puestos preferidos (mayor a menor) cuyos elementos son
        # colas (atributo de Vendedores)

    def ingresar_a_cola(self, vendedor):
        vendedor.cola.append(self)

    def cambiar_de_cola(self, vendedor_anterior, vendedor_nuevo):
        vendedor_anterior.cola.remove(self)
        vendedor_nuevo.cola.append(self)

    def generar_tiempo_llegada_universidad(self, c_llegada):
        self.tiempo_llegada_universidad = triangular(0, 240, c_llegada)


class Alumno(MiembroUC):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)

    def generar_mesada(self, base_mesada):
        self.mesada = base_mesada * (1 + random() ** random()) * 20

    def generar_pesos_diarios(self):
        self.pesos_diarios = self.mesada / 20


class Funcionario(MiembroUC):
    def __init__(self, nombre, apellido, edad, dinero_funcionarios):
        super().__init__(nombre, apellido, edad)
        self.pesos_diarios = dinero_funcionarios
        self.cambios_de_cola = 0

    def reset_cambios_de_cola(self):
        self.cambios_de_cola = 0

    def cambiar_de_cola(self, vendedor_anterior, vendedor_nuevo):
        if self.cambios_de_cola < 3:
            vendedor_anterior.cola.remove(self)
            vendedor_nuevo.cola.append(self)
            self.cambios_de_cola += 1


class Vendedor(Persona):
    def __init__(self, nombre, apellido, edad, producto):
        super().__init__(nombre, apellido, edad)
        self.producto = producto
        self.cola = deque()
        self.contador_stock_out = 0  # cuenta cantidad de veces sin stock
        self.unidades_vendidas = 0
        self.dias_sin_ventas = 0  # dias seguidos
        self.rapidez_atencion = None
        self.stock = None

    def entrega_cola(self):
        def _entrega_cola():
            return self.cola
        return _entrega_cola

    def generar_rapidez_atencion(self, alpha, beta):
        self.rapidez_atencion = randint(alpha, beta)  # en minutos

    def generar_stock(self, alpha, beta):
        self.stock = randint(alpha, beta)

    def tiempo_atencion(self, tiempo_actual):
        return tiempo_actual + self.rapidez_atencion


class Carabinero(Persona):
    def __init__(self, nombre, apellido, edad):
        super().__init__(nombre, apellido, edad)
        self.personalidad = choice(["jekill", "hide"])


class Producto:
    def __init__(self, tipo, precio, calorias):
        pass


cola = deque()
cola.append(1)
cola.append(2)
cola.popleft()
print(cola)
print(expovariate(0.3))