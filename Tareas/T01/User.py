from decimal import Decimal as d
from time import strftime, gmtime
from Order import *

class Usuario:  # de aca se heredan 3 tipos de usuarios
    def __init__(self, username, nombre, apellido, nacimiento):
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.nacimiento = nacimiento  #YYYY-MM-DD
        self.balance_currencies = {"DCC" : d("0")}  # o un diccionario
        self.mercados = []
        self.orders_realizadas = []

    def agregar_mercado(self, mercado):
        self.mercados.append(mercado)

    def generar_balance(self):
        for mercado in self.mercados:
            currency1 = mercado.ticker[0:3]
            currency2 = mercado.ticker[3:]
            if currency1 not in self.balance_currencies.keys():
                self.balance_currencies.update({currency1 : d("0")})
            if currency2 not in self.balance_currencies.keys():
                self.balance_currencies.update({currency2: d("0")})

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
        imprimir = "Usuario: " + self.username + ". Nombre: " + self.nombre + ". Apellido: " + self.apellido
        return imprimir



class Underaged(Usuario):
    def __init__(self, username, nombre, apellido, nacimiento):
        Usuario.__init__(self, username, nombre, apellido, nacimiento)


class Trader(Usuario):
    def __init__(self, username, nombre, apellido, nacimiento):
        Usuario.__init__(self, username, nombre, apellido, nacimiento)

    def ingresar_ask(self, usuario, mercado, divisa_venta, moneda_de_cambio):
        tiempo_actual = strftime("%Y-%m-%d", gmtime())
        nuevo_ask = Ask(usuario, mercado, divisa_venta, moneda_de_cambio, tiempo_actual)
        mercado.orders.append(nuevo_ask)
        mercado.asks.append(nuevo_ask)
        mercado.asks_activos.append(nuevo_ask)
        if mercado.moneda_de_cambio not in usuario.balance_currencies.keys():
            usuario.balance_currencies.update({mercado.moneda_de_cambio : d("0")})
        return nuevo_ask

    def ingresar_bid(self, usuario, mercado, divisa_compra, moneda_de_cambio):
        tiempo_actual = strftime("%Y-%m-%d", gmtime())
        nuevo_bid = Bid(usuario, mercado, divisa_compra, moneda_de_cambio, tiempo_actual)
        mercado.orders.append(nuevo_bid)
        mercado.bids.append(nuevo_bid)
        mercado.bids_activos.append(nuevo_bid)
        if mercado.divisa_compraventa not in usuario.balance_currencies.keys():
            usuario.balance_currencies.update({mercado.divisa_compraventa : d("0")})
        return nuevo_bid

    def transferir_dinero(self, cantidad, usuario_destino, mercado):
        divisa = mercado.ticker[0:3]
        self.balance_currencies[divisa] = int(self.balance_currencies[divisa]) - d(cantidad)
        if divisa not in usuario_destino.balance_currencies.keys():
            usuario_destino.balance_currencies.update({divisa : d("0")})

        usuario_destino.balance_currencies[divisa] = int(usuario_destino.balance_currencies[divisa]) + \
                                                         d(cantidad) * d("0.95")
        mercado.comisiones[divisa] = int(mercado.comisiones[divisa]) + d(cantidad) * d("0.05")




class Investor(Trader):
    def __init__(self, username, nombre, apellido, nacimiento):
        Trader.__init__(self, username, nombre, apellido, nacimiento)

def identificarse(lista_usuarios):
    registro = input("Ingrese\n1 si ya tiene una cuenta registrada\n2 si quiere registrar una nueva cuenta\n")
    if registro == str(2):
        usuario_actual = agregar_usuario(lista_usuarios)
        return usuario_actual
    elif registro == str(1):
        valido = False
        while not valido:
            usuario_ingreso = input("Ingrese su nombre de usuario registrado: ")
            for usuario in lista_usuarios:
                if usuario.username == usuario_ingreso:
                    valido = True
                    usuario_actual = usuario
            if not valido:
                print("El usuario no está registrado.")
        print("Sus orders realizadas hasta el momento son las siguientes:")
        for order in usuario_actual.orders_realizadas:  # HACER LAS ORDERS COMO OBJETOS NO ID
            print("ID:", order)
        print("Su saldo es el siguiente:")
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
    nuevo_nacimiento = input("Ingresa tu fecha de nacimiento (Formato 1990-10-24): ")
    nuevo_usuario = Usuario(nuevo_username, nuevo_nombre, nuevo_apellido, nuevo_nacimiento)
    if nuevo_usuario.determinar_edad() < 18:
        del nuevo_usuario
        nuevo_usuario = Underaged(nuevo_username, nuevo_nombre, nuevo_apellido, nuevo_nacimiento)
    else:
        del nuevo_usuario
        nuevo_usuario = Trader(nuevo_username, nuevo_nombre, nuevo_apellido, nuevo_nacimiento)
    lista_usuarios.append(nuevo_usuario)
    return nuevo_usuario
