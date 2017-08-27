from decimal import Decimal as d
from time import strftime, gmtime
from Order import *


class Usuario:  # de aca se heredan 3 tipos de usuarios
    def __init__(self, username, nombre, apellido, nacimiento):
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self._nacimiento = nacimiento  # YYYY-MM-DD
        self.mercados = []

    @property
    def nacimiento(self):
        return self._nacimiento

    @nacimiento.setter
    def nacimiento(self, value):
        # se usa para no ingresar fechas afuera de 1900 o 2017
        try:
            año = value[0:4]
            mes = value[5:7]
            dia = value[8:]
            int(mes)
            int(dia)
            año_actual = strftime("%Y", gmtime())
            mes_actual = strftime("%m", gmtime())
            dia_actual = strftime("%d", gmtime())
            if int(año) >= 1900 and int(año) < int(año_actual):
                self._nacimiento = value
            elif int(año) == int(año_actual):
                if int(mes) < int(mes_actual):
                    self._nacimiento = value
                elif int(mes) == int(mes_actual):
                    if int(dia) <= int(dia_actual):
                        self._nacimiento = value
            else:
                print("La fecha debe estar entre 1900 y 2017")

            if int(mes) > 12 or int(mes) < 1:
                print("Mes no valido")
                self._nacimiento = ""
            if int(dia) > 31 or int(dia) < 1:
                print("Dia no valido")
                self._nacimiento = ""
        except:
            print("Formato no valido")
            self._nacimiento = ""

    def agregar_mercado(self, mercado):
        self.mercados.append(mercado)
        if mercado.divisa_compraventa not in self.balance_currencies.keys():
            self.balance_currencies.update({mercado.divisa_compraventa :
                                                d("50000")})
            # se agregan los 50.000
        else:
            self.balance_currencies[mercado.divisa_compraventa] += d("50000")
        if mercado.moneda_de_cambio not in self.balance_currencies.keys():
            self.balance_currencies.update({mercado.moneda_de_cambio :
                                                d("50000")})
        else:
            self.balance_currencies[mercado.moneda_de_cambio] += d("50000")

    def determinar_edad(self):
        año = self.nacimiento[0:4]
        mes = self.nacimiento[5:7]
        dia = self.nacimiento[8:]
        año_actual = strftime("%Y", gmtime())
        mes_actual = strftime("%m", gmtime())
        dia_actual = strftime("%d", gmtime())
        diferencia = int(año_actual) - int(año)
        if int(mes_actual) < int(mes):
            return diferencia - 1
        elif int(mes_actual) > int(mes):
            return diferencia
        else:
            if int(dia_actual) < int(dia):
                return diferencia - 1
            else:
                return diferencia

    def __str__(self):
        imprimir = "Usuario: " + self.username + ". Nombre: " + self.nombre \
                   + ". Apellido: " + self.apellido
        return imprimir


class Underaged(Usuario):
    def __init__(self, username, nombre, apellido, nacimiento):
        Usuario.__init__(self, username, nombre, apellido, nacimiento)

    def agregar_mercado(self, mercado):
        # solo agrega el mercado, no se le agrega nada al saldo porque no tiene
        self.mercados.append(mercado)


class Trader(Usuario):
    def __init__(self, username, nombre, apellido, nacimiento):
        Usuario.__init__(self, username, nombre, apellido, nacimiento)
        self.balance_currencies = {"DCC": d("300000")}
        self.orders_realizadas = []  # lista de ids

    def generar_balance(self):  # agregar al diccionario de balances a
                                #  partir de los mercados registrados
        for mercado in self.mercados:
            currency1 = mercado.ticker[0:3]
            currency2 = mercado.ticker[3:]
            if currency1 not in self.balance_currencies.keys():
                self.balance_currencies.update({currency1: d("0")})
            if currency2 not in self.balance_currencies.keys():
                self.balance_currencies.update({currency2: d("0")})

    def ingresar_ask(self, usuario, mercado, divisa_venta, moneda_de_cambio):
        tiempo_actual = strftime("%Y-%m-%d", gmtime())
        nuevo_ask = Ask(usuario, mercado, divisa_venta, moneda_de_cambio,
                        tiempo_actual)
        mercado.orders.append(nuevo_ask)
        mercado.asks.append(nuevo_ask)
        mercado.asks_activos.append(nuevo_ask)
        if mercado.moneda_de_cambio not in usuario.balance_currencies.keys():
            usuario.balance_currencies.update({mercado.moneda_de_cambio :
                                                   d("0")})
        return nuevo_ask

    def ingresar_bid(self, usuario, mercado, divisa_compra, moneda_de_cambio):
        tiempo_actual = strftime("%Y-%m-%d", gmtime())
        nuevo_bid = Bid(usuario, mercado, divisa_compra, moneda_de_cambio,
                        tiempo_actual)
        mercado.orders.append(nuevo_bid)
        mercado.bids.append(nuevo_bid)
        mercado.bids_activos.append(nuevo_bid)
        if mercado.divisa_compraventa not in usuario.balance_currencies.keys():
            usuario.balance_currencies.update({mercado.divisa_compraventa:
                                                   d("0")})
        return nuevo_bid

    def transferir_dinero(self, cantidad, usuario_destino, mercado):
        divisa = mercado.ticker[0:3]
        if d(self.balance_currencies[divisa]) - d(cantidad) < 0:
            print("No tienes dinero suficiente para realizar la transferencia.")
            return
        self.balance_currencies[divisa] = d(self.balance_currencies[divisa]) -\
                                          d(str(cantidad))
        if divisa not in usuario_destino.balance_currencies.keys():
            usuario_destino.balance_currencies.update({divisa: d("0")})

        usuario_destino.balance_currencies[divisa] = d(usuario_destino.
                                                       balance_currencies[
                                                           divisa]) + \
                                                         d(cantidad) * \
                                                         d("0.95")
        mercado.comisiones[divisa] = d(mercado.comisiones[divisa]) + \
                                     d(cantidad) * d("0.05")


class Investor(Trader):
    def __init__(self, username, nombre, apellido, nacimiento):
        Trader.__init__(self, username, nombre, apellido, nacimiento)

    def desplegar_balance_historico(self, lista_orders):
        for order in lista_orders:
            if order.usuario.username == self.username:
                if order.ejecutada:
                    if isinstance(order, Ask):
                        perdida = d(order.divisa_venta)
                        ganancia = (d(order.divisa_venta) *
                                    d(order.moneda_de_cambio) *
                                    order.mercado.determinar_tasa(self))
                        print("Con la order", order.id, "el dia",
                              order.match_time, "ganaste", str(ganancia),
                              order.mercado.moneda_de_cambio, "y perdiste",
                              str(perdida), order.mercado.divisa_compraventa)
                    elif isinstance(order, Bid):
                        ganancia = d(order.divisa_compra) * \
                                   order.mercado.determinar_tasa(self)
                        perdida = d(order.divisa_compra) *\
                                  d(order.moneda_de_cambio)
                        print("Con la order", order.id, "el dia",
                              order.match_time, "ganaste", str(ganancia),
                              order.mercado.moneda_de_cambio, "y perdiste",
                              str(perdida), order.mercado.divisa_compraventa)


def identificarse(lista_usuarios):
    while True:  # manejo de errores
        registro = input("Ingrese\n1 si ya tiene una cuenta registrada\n2 "
                         "si quiere registrar una nueva cuenta\n")
        if registro != "1" and registro != "2":
            print("Opcion invalida")
        else:
            break
    if registro == str(2):
        usuario_actual = agregar_usuario(lista_usuarios)
        return usuario_actual
    elif registro == str(1):
        valido = False
        while not valido:
            usuario_ingreso = input("Ingrese su nombre de usuario registrado "
                                    "(0 para registrarse): ")
            if usuario_ingreso == "0":
                usuario_actual = identificarse(lista_usuarios)
                return usuario_actual
            for usuario in lista_usuarios:
                if usuario.username == usuario_ingreso:
                    valido = True
                    usuario_actual = usuario
            if not valido:
                print("El usuario no está registrado.")
        print("\nSu saldo es el siguiente:")
        if isinstance(usuario_actual, Trader):
            for symbol, saldo in usuario_actual.balance_currencies.items():
                print(symbol, saldo)
        return usuario_actual


def agregar_usuario(lista_usuarios):
    existe = False
    nuevo_username = input("Ingresa tu nombre de usuario: ")
    for usuario in lista_usuarios:
        if usuario.username == nuevo_username:
            existe = True
            print("El nombre de usuario ya existe. Elige otro.")
            nuevo_usuario = agregar_usuario(lista_usuarios)
            return nuevo_usuario
    nuevo_nombre = input("Ingresa tu nombre: ")
    nuevo_apellido = input("Ingresa tu apellido: ")
    nuevo_usuario = Usuario(nuevo_username, nuevo_nombre, nuevo_apellido, "")
    while nuevo_usuario.nacimiento == "":
        nuevo_nacimiento = input("Ingresa tu fecha de nacimiento "
                                 "(Formato 1990-10-24): ")
        nuevo_usuario.nacimiento = nuevo_nacimiento
    if nuevo_usuario.determinar_edad() < 18:
        del nuevo_usuario
        nuevo_usuario = Underaged(nuevo_username, nuevo_nombre, nuevo_apellido,
                                  nuevo_nacimiento)
    else:
        del nuevo_usuario
        nuevo_usuario = Trader(nuevo_username, nuevo_nombre, nuevo_apellido,
                               nuevo_nacimiento)
        nuevo_usuario.balance_currencies["DCC"] = d("100000")
    lista_usuarios.append(nuevo_usuario)
    return nuevo_usuario
