from User import *
from csv_reader import read, write_ordenado
from Order import *
from Mercado import Mercado, Moneda
from decimal import Decimal as d

class Sistema:
    def __init__(self, lista_usuarios, lista_mercados, lista_orders, lista_monedas, lista_match):
        self.lista_usuarios = lista_usuarios
        self.lista_mercados = lista_mercados
        self.lista_orders = lista_orders
        self.lista_monedas = lista_monedas
        self.lista_match = lista_match

    def start(self):
        usuario_actual = identificarse(self.lista_usuarios)
        while True:
            opcion = self.desplegar_menu(usuario_actual)
            if opcion == "10":
                return
            elif opcion == "1":
                self.desplegar_mercados(True, usuario_actual)
            elif opcion == "2":
                self.desplegar_mercados(False, usuario_actual)
            elif opcion == "3":
                mercado_a_registrar = input("Ingrese el ticker del mercado al que se quiere registrar: ")
                for mercado in lista_mercados:
                    if mercado_a_registrar == mercado.ticker:
                        mercado_a_registrar = mercado
                        break
                usuario_actual.agregar_mercado(mercado_a_registrar)
            elif opcion == "4":
                print("1: Desplegar orders en una fecha especifica\n2: Desplegar orders entre 2 fechas\n"
                      "3: Desplegar orders en un mercado especifico")
                opcion_desplegar_orders = input("Ingrese una de las 3 opciones: ")
                if opcion_desplegar_orders == "1":
                    fecha1 = input("Ingrese la fecha especifica (YYYY-MM-DD): ")
                    fecha2 = ""
                    for order in lista_orders:
                        order.desplegar_order_por_fecha(fecha1, fecha2)
                elif opcion_desplegar_orders == "2":
                    fecha1 = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                    fecha2 = input("Ingrese la fecha final (YYYY-MM-DD): ")
                    for order in lista_orders:
                        order.desplegar_order_por_fecha(fecha1, fecha2)
                elif opcion_desplegar_orders == "3":
                    mercado_a_desplegar = input("Ingrese el ticker del mercado a observar: ")
                    for mercado in lista_mercados:
                        if mercado_a_desplegar == mercado.ticker:
                            mercado_a_desplegar = mercado
                            break
                    for order in lista_orders:
                        order.desplegar_order_por_mercado(mercado_a_desplegar)
            elif opcion == "5":
                for mercado in lista_mercados:
                    if mercado.asks_activos != [] or mercado.bids_activos != []:
                        print("MERCADO:", mercado.ticker)
                    for order in mercado.asks_activos:
                        print(order)
                    for order in mercado.bids_activos:
                        print(order)
            elif opcion == "6":
                mercado_actual = input("Ingrese el ticker del mercado para hacer un ask: ")
                for mercado in lista_mercados:
                    if mercado.ticker == mercado_actual:
                        mercado_actual = mercado
                        break
                divisa_venta = input("Ingrese la cantidad de " + mercado_actual.ticker[0:3] + " que quieres vender: ")
                moneda_de_cambio = input("Ingrese el precio en " + mercado_actual.ticker[3:] +
                                         " al que vendes una unidad: ")
                nuevo_ask = usuario_actual.ingresar_ask(usuario_actual, mercado_actual, divisa_venta, moneda_de_cambio)
                maximo = self.maximo_id()
                nuevo_ask.id = str(maximo + 1)
                lista_orders.append(nuevo_ask)
                self.determinar_match(usuario_actual, nuevo_ask)
                print(usuario_actual.balance_currencies)
            elif opcion == "7":
                mercado_actual = input("Ingrese el ticker del mercado para hacer un bid: ")
                for mercado in lista_mercados:
                    if mercado.ticker == mercado_actual:
                        mercado_actual = mercado
                        break
                divisa_compra = input("Ingrese la cantidad de " + mercado_actual.ticker[0:3] + " que quieres comprar: ")
                moneda_de_cambio = input("Ingrese el precio en " + mercado_actual.ticker[3:] +
                                         " al que compras una unidad: ")
                nuevo_bid = usuario_actual.ingresar_bid(usuario_actual, mercado_actual, divisa_compra, moneda_de_cambio)
                maximo = self.maximo_id()
                nuevo_bid.id = str(maximo + 1)
                lista_orders.append(nuevo_bid)
            elif opcion == "8":
                print("1 : Informacion de todos los mercados")
                print("2 : Informacion de un mercado en especifico")
                opcion = input("Ingrese una de las 2 opciones: ")
                if opcion == "1":
                    for mercado in lista_mercados:
                        mercado.desplegar_informacion()
                elif opcion == "2":
                    mercado_elegido = input("Ingrese el ticker del mercado especifico: ")
                    for mercado in lista_mercados:
                        if mercado.ticker == mercado_elegido:
                            mercado_elegido = mercado
                            mercado_elegido.desplegar_informacion()
                            break
            elif opcion == "9":
                usuario_destino = input("Ingresa el nombre de usuario del destinatario: ")
                for usuario in lista_usuarios:
                    if usuario.username == usuario_destino:
                        usuario_destino = usuario
                        break
                print(usuario_destino.balance_currencies)
                monto = input("Ingresa el monto a transferir (ej.: 100 DCC): ")
                numero = True
                cantidad = ""
                simbolo = ""
                for letra in monto:
                    if numero and letra != " ":
                        cantidad += letra
                    elif not numero:
                        simbolo += letra
                    if letra == " ":
                        numero = False
                print(simbolo)
                for mercado in lista_mercados:
                    if mercado.divisa_compraventa == simbolo:
                        mercado_comision = mercado
                        break
                usuario_actual.transferir_dinero(cantidad, usuario_destino, mercado_comision)
                print(usuario_destino.balance_currencies)
            elif opcion == "11":
                lista_underaged = []
                lista_trader = []
                lista_investor = []
                for usuario in lista_usuarios:
                    if isinstance(usuario, Underaged):
                        lista_underaged.append(usuario)
                    else:
                        if isinstance(usuario, Investor):
                            lista_investor.append(usuario)
                        else:
                            lista_trader.append(usuario)
                print("Usuarios Underaged:")
                for usuario in lista_underaged:
                    print("    ", usuario)
                print("Usuarios Trader:")
                for usuario in lista_trader:
                    print("{}{}".format("    ", usuario))

                print("Usuarios Investor:")
                for usuario in lista_investor:
                    print("    ", usuario)

    def maximo_id(self):
        maximo = 0
        for order in self.lista_orders:
            if int(order.id) > maximo:
                maximo = int(order.id)
        return maximo

    def desplegar_menu(self, usuario_actual):
        print("-" * 10 + " MENU " + str(usuario_actual.username) + " " + "-" * 10)
        print("1 :  Lista de mercados disponibles")
        print("2 :  Lista de mercados registrados")
        print("3 :  Registrarse en un mercado especifico")
        print("4 :  Lista de orders")
        print("5 :  Lista de orders activas")
        print("6 :  Ingresar ask")
        print("7 :  Ingresar bid")
        print("8 :  Desplegar informacion de un mercado")
        print("9 :  Banco")
        print("10 :  Salir del sistema")
        print("11:  Consultas")
        opcion = input("Ingrese su numero de opcion a seguir: ")
        return opcion

    def desplegar_mercados(self, todos, usuario_actual):
        if todos:
            print("MERCADOS DISPONIBLES:")
            for mercado in self.lista_mercados:
                print("->" + mercado.ticker)
        else:
            print("MERCADOS REGISTRADOS:")
            for mercado in usuario_actual.mercados:
                print("->" + mercado.ticker)

    def determinar_match(self, usuario_actual, order_realizada):
        mercado = order_realizada.mercado
        asks = []
        bids = []
        for order in self.lista_orders:
            if order.mercado == mercado and order != order_realizada and order.ejecutada == False:
                if isinstance(order, Ask):
                    asks.append(order)
                elif isinstance(order, Bid):
                    bids.append(order)
        still_left = True  # variable que es False cuando ya no hay mas match posible con la order realizada
        #while still_left:

        if isinstance(order_realizada, Ask):  # en caso de que se ponga un Ask
            opciones_bids = []  # bids que le convienen a la compra
            for bid in bids:
                if bid.moneda_de_cambio >= order_realizada.moneda_de_cambio:
                    opciones_bids.append(bid)
            if len(opciones_bids) == 0:  # no hay match
                return
            opciones_bids.sort(key=lambda elem: float(elem.moneda_de_cambio), reverse = True)
            mejores_opciones = [opciones_bids.pop(0)]
            for bid in opciones_bids:
                if bid.moneda_de_cambio == mejores_opciones[0].moneda_de_cambio:
                    mejores_opciones.append(bid)
            if len(mejores_opciones) == 1:
                mejor_opcion = mejores_opciones[0]
            elif len(mejores_opciones) > 1:
                mejores_opciones.sort(key=lambda elem: (int(elem.año),int(elem.mes), int(elem.dia)))
                mejor_opcion = mejores_opciones[0]

            if d(order_realizada.divisa_venta) <= d(mejor_opcion.divisa_compra):
                still_left = False
                usuario_actual.balance_currencies[mercado.divisa_compraventa] -= d(order_realizada.divisa_venta)
                usuario_actual.balance_currencies[mercado.moneda_de_cambio] += (d(order_realizada.divisa_venta) *
                                                                                d(mejor_opcion.moneda_de_cambio))
                mejor_opcion.usuario.balance_currencies[mercado.divisa_compraventa] += d(order_realizada.divisa_venta)
                print(mejor_opcion.moneda_de_cambio)
                mejor_opcion.usuario.balance_currencies[mercado.moneda_de_cambio] -= (d(order_realizada.divisa_venta)
                                                                                     * d(mejor_opcion.moneda_de_cambio))
                mercado.asks_activos.remove(order_realizada)
                mercado.bids_activos.remove(mejor_opcion)
                order_realizada.ejecutada = True
                mejor_opcion.ejecutada = True
                resto = d(mejor_opcion.divisa_compra) - d(order_realizada.divisa_venta)
                if resto != 0:
                    new_bid = Bid(mejor_opcion.usuario, mercado, float(resto), mejor_opcion.moneda_de_cambio,
                                  mejor_opcion.tiempo)
                    maximo = self.maximo_id()
                    new_bid.id = str(maximo + 1)
                    self.lista_orders.append(new_bid)
                    mercado.bids_activos.append(new_bid)
                    mercado.orders.append(new_bid)  # quitamos el resto de la order
                    mejor_opcion.divisa_compra = d(mejor_opcion.divisa_compra) - d(resto)
            elif d(order_realizada.divisa_venta) > d(mejor_opcion.divisa_compra):
                usuario_actual.balance_currencies[mercado.divisa_compraventa] -= d(mejor_opcion.divisa_compra)
                usuario_actual.balance_currencies[mercado.moneda_de_cambio] += (d(mejor_opcion.divisa_compra) *
                                                                                 d(mejor_opcion.moneda_de_cambio))
                mejor_opcion.usuario.balance_currencies[mercado.divisa_compraventa] += d(mejor_opcion.divisa_compra)
                mejor_opcion.usuario.balance_currencies[mercado.moneda_de_cambio] -= (d(mejor_opcion.divisa_compra)
                                                                                     * d(mejor_opcion.moneda_de_cambio))
                resto = d(order_realizada.divisa_venta) - d(mejor_opcion.divisa_compra)
                mercado.asks_activos.remove(order_realizada)
                mercado.bids_activos.remove(mejor_opcion)
                order_realizada.ejecutada = True
                mejor_opcion.ejecutada = True
                new_ask = Ask(order_realizada.usuario, mercado, float(resto), order_realizada.moneda_de_cambio,
                              order_realizada.tiempo)
                maximo = self.maximo_id()
                new_ask.id = str(maximo + 1)
                self.lista_orders.append(new_ask)
                mercado.asks_activos.append(new_ask)
                mercado.orders.append(new_ask)
                order_realizada.divisa_venta = d(order_realizada.divisa_venta) - d(resto)
            if still_left:
                self.determinar_match(usuario_actual, new_ask)
        #if isinstance(order_realizada, Bid):  # en caso de que se ponga un Bid




def poblar_sistema(archivo, lista_usuarios, lista_mercados):
    if archivo == "users.csv":
        lista_info_usuarios = read(archivo)
        for info_usuario in lista_info_usuarios:
            usuario = Usuario(info_usuario["username"], info_usuario["name"], info_usuario["lastname"],
                              info_usuario["birthday"])
            if usuario.determinar_edad() < 18:
                del usuario
                usuario = Underaged(info_usuario["username"], info_usuario["name"], info_usuario["lastname"],
                              info_usuario["birthday"])
            else:
                del usuario
                usuario = Trader(info_usuario["username"], info_usuario["name"], info_usuario["lastname"],
                                 info_usuario["birthday"])
            usuario.orders_realizadas = info_usuario["orders"]
            lista_usuarios.append(usuario)
        return lista_usuarios
    elif archivo == "Currencies.csv":
        lista_info_monedas = read(archivo)
        lista_monedas = []
        for info_moneda in lista_info_monedas:
            moneda = Moneda(info_moneda["symbol"], info_moneda["name"])
            lista_monedas.append(moneda)
        return lista_monedas
    elif archivo == "orders.csv":
        global lista_asks
        global lista_bids
        lista_info_orders = read(archivo)
        lista_info_orders = write_ordenado(lista_info_orders)
        lista_orders = []
        lista_asks = []
        lista_bids = []
        lista_matches = []
        for info_order in lista_info_orders:
            for mercado in lista_mercados:  # se usara para saber a que mercado pertenece la order
                if mercado.ticker == info_order["ticker"]:
                    mercado_order = mercado
            for usuario in lista_usuarios:  # se usara para saber a que usuario pertenece la order
                if info_order["order_id"] in usuario.orders_realizadas:
                    if info_order["type"] == "ask":
                        divisas = info_order["ticker"]

                        order = Ask(usuario, mercado_order, info_order["amount"], info_order["price"],
                                    info_order["date_created"])
                        # el mercado puede ser un objeto tambien
                        if info_order["date_match"] == "":
                            mercado_order.asks_activos.append(order)
                        else:
                            order.ejecutada = True
                            pass  # MATCH
                        mercado_order.asks.append(order)
                        lista_asks.append(order)

                    elif info_order["type"] == "bid":
                        divisas = info_order["ticker"]
                        order = Bid(usuario, mercado_order, info_order["amount"], info_order["price"],
                                    info_order["date_created"])
                        # el mercado puede ser un objeto tambien
                        if info_order["date_match"] == "":
                            mercado_order.bids_activos.append(order)
                        else:
                            order.ejecutada = True
                            pass  # MATCH
                        lista_bids.append(order)
                        mercado_order.bids.append(order)
                    if mercado_order not in usuario.mercados:
                        usuario.agregar_mercado(mercado_order)
                    mercado_order.orders.append(order)
                    order.id = info_order["order_id"]
                    order.match_time = info_order["date_match"]
                    lista_orders.append(order)
        return lista_orders


def generar_mercados(lista_monedas):
    lista_mercados = []
    for moneda1 in lista_monedas:
        for moneda2 in lista_monedas:
            if moneda1.simbolo != moneda2.simbolo:
                ticker = moneda1.simbolo + moneda2.simbolo
                mercado = Mercado(ticker)
                lista_mercados.append(mercado)
    return lista_mercados


def poblar_balances(lista_mercados):  # se considera solo la informacion en las orders para saber el presupuesto de
    for mercado in lista_mercados:  # los usuarios (es decir, si hay 1000 clp en venta, ese usuario tiene 1000 clp)
        divisa_intercambio = mercado.ticker[0:3]
        moneda_de_cambio = mercado.ticker[3:]
        for ask in mercado.asks:
            venta = ask.divisa_venta
            ask.usuario.balance_currencies[divisa_intercambio] += d(venta)
        for bid in mercado.bids:
            paga = d(bid.moneda_de_cambio) * d(bid.divisa_compra)
            bid.usuario.balance_currencies[moneda_de_cambio] += d(paga)


def determinar_match_bases(lista_mercados):  # sirve para ver los match que ya ocurrieron en los csv,
    lista_match = []
    for mercado in lista_mercados:                     # y asi poder actualizar las currencies de los usuarios
        divisa_compraventa = mercado.ticker[0:3]
        divisa_moneda_de_cambio = mercado.ticker[3:]
        for ask in mercado.asks:
            if ask.match_time != "":
                for bid in mercado.bids:
                    if ask.match_time == bid.match_time:  # hubo intercambio
                        print(mercado.ticker, "ASK", ask.id, ask.tiempo, ask.usuario.username, "BID", bid.id,
                              bid.tiempo, bid.usuario.username)
                        new_match = Match(ask, bid, ask.match_time)
                        lista_match.append(new_match)
                        precio_transado = str(min(float(ask.moneda_de_cambio), float(bid.moneda_de_cambio)))
                        if ask.divisa_venta <= bid.divisa_compra:
                            venta = d(precio_transado) * d(ask.divisa_venta)
                            ask.usuario.balance_currencies[divisa_compraventa] -= d(ask.divisa_venta)
                            ask.usuario.balance_currencies[divisa_moneda_de_cambio] += (venta)
                            bid.usuario.balance_currencies[divisa_compraventa] += d(ask.divisa_venta)
                            bid.usuario.balance_currencies[divisa_moneda_de_cambio] -= venta

                        elif ask.divisa_venta >= bid.divisa_compra:
                            compra = d(precio_transado) * d(ask.divisa_compra)
                            ask.usuario.balance_currencies[divisa_compraventa] -= d(ask.divisa_compra)
                            ask.usuario.balance_currencies[divisa_moneda_de_cambio] += compra
                            bid.usuario.balance_currencies[divisa_compraventa] += d(ask.divisa_compra)
                            bid.usuario.balance_currencies[divisa_moneda_de_cambio] -= compra
    return lista_match


lista_usuarios = poblar_sistema("users.csv", [], [])
lista_monedas = poblar_sistema("Currencies.csv", lista_usuarios, [])
lista_monedas.append(Moneda("DCC", "DCC CryptoCoin"))  # creamos la moneda oficial que no viene en csv
lista_mercados = generar_mercados(lista_monedas)
lista_orders = poblar_sistema("orders.csv", lista_usuarios, lista_mercados)

for usuario in lista_usuarios:
    usuario.generar_balance()

poblar_balances(lista_mercados)

for usuario in lista_usuarios:
    print(usuario.username, usuario.balance_currencies)
print("-"*50)

lista_match = determinar_match_bases(lista_mercados)

esta = False
for usuario in lista_usuarios:
    if "96" in usuario.orders_realizadas:
        esta = True
    print(usuario.username, usuario.determinar_edad(), isinstance(usuario, Underaged), usuario.balance_currencies)
print(esta)
sistema = Sistema(lista_usuarios, lista_mercados, lista_orders, lista_monedas, lista_match)

sistema.start()

for mercado in lista_mercados:
    for ask in mercado.asks_activos:
        print(ask.id)
    for bid in mercado.bids_activos:
        print(bid.id)