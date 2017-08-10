class Ciudad:

    def __init__(self, nombre):
        self.nombre = nombre
        self.comunas = []


class Comuna:

    def __init__(self, nombre):
        self.nombre = nombre
        self.casas_edificios = []

    def agregar_vivienda(self, Vivienda):
        if isinstance(Vivienda, Casa) or isinstance(Vivienda, Edificio):
            self.casas_edificios.append(Vivienda)
        else:
            print("Tipo de vivienda no válido.")

    def __repr__(self):
        contador_electro = 0
        contador_consumo = 0
        for vivienda in self.casas_edificios:
            if vivienda.electro_dependiente == True:
                contador_electro += 1
            ultimo_consumo = len(vivienda.medidor) - 1
            contador_consumo += vivienda.medidor[ultimo_consumo]
        return ("Hay " + str(len(self.casas_edificios)) + " medidores en la comuna " + self.nombre + ", " +
                str(contador_electro) + " electrodependientes y el ultimo consumo fue de " + str(contador_consumo))


class Casa:

    def __init__(self, direccion, cliente):
        self.direccion = direccion
        self._electro_dependiente = False
        self.cliente = cliente
        self.medidor = []

    def agregar_consumo(self, consumo):
        if consumo >= 0 and consumo <= 5000:
            self.medidor.append(consumo)
        else:
            print("Consumo no válido.")

    @property
    def electro_dependiente(self):
        return self._electro_dependiente

    @electro_dependiente.setter
    def electro_dependiente(self, boolean):
        if type(boolean) == int:
            if boolean == 1:
                self._electro_dependiente = True
            elif boolean == 0:
                self._electro_dependiente = False
            else:
                print("Valor invalido electrodependiente.")
        elif type(boolean) == bool:
            self._electro_dependiente = boolean


    def __repr__(self):
        ultimo_consumo = len(self.medidor) - 1
        consumo = self.medidor[ultimo_consumo]
        return ("El ultimo consumo de la casa del cliente " + str(self.cliente) + " fue de " + str(consumo) + "."
                + " Electrodependiente: " + str(self._electro_dependiente))


class Edificio:

    def __init__(self, direccion, nombre):
        self.direccion = direccion
        self.nombre = nombre
        self.medidor = []
        self.departamentos = []
        self._electro_dependiente = 0  ## cantidad de electrodependientes en el edificio

    def agregar_consumo(self, consumo):
        if consumo >= 0 and consumo <= 10000:
            self.medidor.append(consumo)
        else:
            print("Consumo no válido.")

    @property
    def electro_dependiente(self):
        for departamento in self.departamentos:
            if departamento._electro_dependiente == True:
                self._electro_dependiente += 1

    def __repr__(self):
        ultimo = len(self.medidor) - 1
        ultimo_consumo = self.medidor(ultimo)
        consumo_total = 0
        for consumo in medidor:
            consumo_total += consumo
        contador_electro = 0
        for departamento in self.departamentos:
            if departamento._electro_dependiente == True:
                contador_electro += 1
        return ("El ultimo consumo comun del edificio " + str(self.nombre) + " fue de " + str(ultimo_consumo) +
                " y total de " + str(consumo_total) + ". Hay " + str(contador_electro) + " electrodependientes.")

class Departamento:

    def __init__(self, numero, cliente):
        self.medidor = []
        self.numero = numero
        self._electro_dependiente = False
        self.cliente = cliente

    def agregar_consumo(self, consumo):
        if consumo >= 0 and consumo <= 4000:
            self.medidor.append(consumo)
        else:
            print("Consumo no válido.")

    @property
    def electro_dependiente(self):
        return self._electro_dependiente
    @electro_dependiente.setter

    def electro_dependiente(self, boolean):
        if type(boolean) == int:
            if boolean == 1:
                self._electro_dependiente = True
            elif boolean == 0:
                self._electro_dependiente = False
            else:
                print("Valor invalido electrodependiente.")
        elif type(boolean) == bool:
            self._electro_dependiente = boolean


    def __repr__(self):
        ultimo_consumo = len(self.medidor) - 1
        consumo = self.medidor[ultimo_consumo]
        return ("El ultimo consumo del departamento del cliente " + str(self.cliente) + " fue de " + str(consumo) + "."
                + " Electrodependiente: " + str(self._electro_dependiente))

class Cliente:

    def __init__(self, nombre, rut):
        self.nombre = nombre
        self.rut = rut

class Medidor:

    def __init__(self):
        self.consumo = []

    def agregar_consumo(self, consumo):
        a = 0

cliente1 = Cliente("Max", "123-k")
cliente2 = Cliente("Alex", "124-k")
casa1 = Casa("San joaquin", cliente1)
casa1.electro_dependiente = True
print(casa1._electro_dependiente)
edificio1 = Edificio("Benito Rebolledo", "Angelini")
departamento1 = Departamento("55", cliente2)
edificio1.departamentos.append(departamento1)
departamento1.electro_dependiente = True
comuna1 = Comuna("Macul")
comuna1.agregar_vivienda(casa1)
comuna1.agregar_vivienda(cliente1)  ## error
comuna1.agregar_vivienda(edificio1)
casa1.agregar_consumo(1000)
casa1.agregar_consumo(10000)  ## error
edificio1.agregar_consumo(5000)
ciudad1 = Ciudad("Santiago")
ciudad1.comunas.append(comuna1)



print(comuna1)