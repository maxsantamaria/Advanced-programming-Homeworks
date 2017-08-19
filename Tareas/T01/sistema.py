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
        self.estado_orders(usuario_actual)
        while True:
            opcion = self.desplegar_menu(usuario_actual)
            if opcion == "8":
                return
            elif opcion == "1":
                self.desplegar_mercados(True, usuario_actual)
            elif opcion == "2":
                self.desplegar_mercados(False, usuario_actual)
            elif opcion == "3":
                mercado_a_registrar = input("Ingrese el ticker del mercado al que se quiere registrar: ")
                for mercado in self.lista_mercados:
                    if mercado_a_registrar == mercado.ticker:
                        mercado_a_registrar = mercado
                        break
                usuario_actual.agregar_mercado(mercado_a_registrar)
            elif opcion == "10":
                print("1: Desplegar orders en una fecha especifica\n2: Desplegar orders entre 2 fechas\n"
                      "3: Desplegar orders en un mercado especifico")
                opcion_desplegar_orders = input("Ingrese una de las 3 opciones: ")
                if opcion_desplegar_orders == "1":
                    fecha1 = input("Ingrese la fecha especifica (YYYY-MM-DD): ")
                    fecha2 = ""
                    for order in self.lista_orders:
                        order.desplegar_order_por_fecha(fecha1, fecha2)
                elif opcion_desplegar_orders == "2":
                    fecha1 = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                    fecha2 = input("Ingrese la fecha final (YYYY-MM-DD): ")
                    for order in self.lista_orders:
                        order.desplegar_order_por_fecha(fecha1, fecha2)
                elif opcion_desplegar_orders == "3":
                    mercado_a_desplegar = input("Ingrese el ticker del mercado a observar: ")
                    for mercado in self.lista_mercados:
                        if mercado_a_desplegar == mercado.ticker:
                            mercado_a_desplegar = mercado
                            break
                    for order in self.lista_orders:
                        order.desplegar_order_por_mercado(mercado_a_desplegar)
            elif opcion == "5":
                for mercado in self.lista_mercados:
                    if mercado.asks_activos != [] or mercado.bids_activos != []:
                        print("MERCADO:", mercado.ticker)
                    for order in mercado.asks_activos:
                        print(order)
                    for order in mercado.bids_activos:
                        print(order)
            elif opcion == "13":
                mercado_actual = input("Ingrese el ticker del mercado para hacer un ask: ")
                for mercado in self.lista_mercados:
                    if mercado.ticker == mercado_actual:
                        mercado_actual = mercado
                        break
                divisa_venta = input("Ingrese la cantidad de " + mercado_actual.ticker[0:3] + " que quieres vender: ")
                moneda_de_cambio = input("Ingrese el precio en " + mercado_actual.ticker[3:] +
                                         " al que vendes una unidad: ")
                nuevo_ask = usuario_actual.ingresar_ask(usuario_actual, mercado_actual, divisa_venta, moneda_de_cambio)
                maximo = self.maximo_id()
                nuevo_ask.id = str(maximo + 1)
                self.lista_orders.append(nuevo_ask)
                self.determinar_match(usuario_actual, nuevo_ask)
                print(usuario_actual.balance_currencies)
            elif opcion == "12":
                mercado_actual = input("Ingrese el ticker del mercado para hacer un bid: ")
                for mercado in self.lista_mercados:
                    if mercado.ticker == mercado_actual:
                        mercado_actual = mercado
                        break
                divisa_compra = input("Ingrese la cantidad de " + mercado_actual.ticker[0:3] + " que quieres comprar: ")
                moneda_de_cambio = input("Ingrese el precio en " + mercado_actual.ticker[3:] +
                                         " al que compras una unidad: ")
                nuevo_bid = usuario_actual.ingresar_bid(usuario_actual, mercado_actual, divisa_compra, moneda_de_cambio)
                maximo = self.maximo_id()
                nuevo_bid.id = str(maximo + 1)
                self.lista_orders.append(nuevo_bid)
                self.determinar_match(usuario_actual, nuevo_bid)
                print(usuario_actual.balance_currencies)
            elif opcion == "4":
                print("1 : Informacion de todos los mercados")
                print("2 : Informacion de un mercado en especifico")
                opcion = input("Ingrese una de las 2 opciones: ")
                if opcion == "1":
                    for mercado in self.lista_mercados:
                        mercado.desplegar_informacion()
                elif opcion == "2":
                    mercado_elegido = input("Ingrese el ticker del mercado especifico: ")
                    for mercado in self.lista_mercados:
                        if mercado.ticker == mercado_elegido:
                            mercado_elegido = mercado
                            mercado_elegido.desplegar_informacion()
                            break
            elif opcion == "11":
                usuario_destino = input("Ingresa el nombre de usuario del destinatario: ")
                for usuario in self.lista_usuarios:
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
                for mercado in self.lista_mercados:
                    if mercado.divisa_compraventa == simbolo:
                        mercado_comision = mercado
                        break
                usuario_actual.transferir_dinero(cantidad, usuario_destino, mercado_comision)
                print(usuario_destino.balance_currencies)
            elif opcion == "9":
                print("1: Informacion de todos los usuarios\n2: Historial de matches\n3: Informacion de monedas")
                opcion_consulta = input("Ingrese la opcion de la consulta a realizar: ")
                if opcion_consulta == "1":
                    lista_underaged = []
                    lista_trader = []
                    lista_investor = []
                    for usuario in self.lista_usuarios:
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
                elif opcion_consulta == "2":
                    print("Lista de match hasta el momento:")
                    for match in self.lista_match:
                        print(match.ask)
                        print(match.bid, "\n")
                elif opcion_consulta == "3":
                    for moneda in self.lista_monedas:
                        print(moneda)
                    mercados_activos = 0
                    for mercado in self.lista_mercados:
                        if len(mercado.asks_activos) != 0 or len(mercado.bids_activos) != 0:
                            mercados_activos += 1
                    print("Hay " + str(mercados_activos) + " mercados con orders activas en este momento")
                    for mercado in self.lista_mercados:
                        match_en_mercado = []
                        for match in self.lista_match:
                            if match.ask.mercado == mercado:
                                match_en_mercado.append(match)
                        if match_en_mercado != []:
                            match_en_mercado.sort(key=lambda elem: (int(elem.año),int(elem.mes), int(elem.dia)),
                                                  reverse = True)
                            ultimo_match = match_en_mercado[0]
                            print("Precio actual de", mercado.divisa_compraventa, "en mercado", mercado.ticker, ":",
                                  ultimo_match.bid.moneda_de_cambio, mercado.moneda_de_cambio)
                            print("    Ultimo match -> ", ultimo_match.tiempo)


            elif opcion == "7":
                print("Has cerrado sesión. \n")
                usuario_actual = identificarse(self.lista_usuarios)
                self.estado_orders(usuario_actual)
            elif opcion == "6":
                print("Su saldo es el siguiente:")
                for symbol, saldo in usuario_actual.balance_currencies.items():
                    print(symbol, saldo)
            elif opcion == "14":  # upgrade
                pass
    def upgrade(self, usuario_actual):
        pass

    def maximo_id(self):
        maximo = 0
        for order in self.lista_orders:
            if int(order.id) > maximo:
                maximo = int(order.id)
        return maximo

    def desplegar_menu(self, usuario_actual):
        invalido = True
        print("-" * 10 + " MENU " + str(usuario_actual.username) + " " + "-" * 10)
        print("1 :  Lista de mercados disponibles")
        print("2 :  Lista de mercados registrados")
        print("3 :  Registrarse en un mercado especifico")
        print("4 :  Desplegar informacion de un mercado")
        print("5 :  Lista de orders activas")
        print("6 :  Consulta de saldo")
        print("7 :  Cerrar sesión")
        print("8 :  Salir del sistema")
        if isinstance(usuario_actual, Trader):
            print("9 :  Consultas")
            print("10:  Lista de orders")
            print("11:  Banco")
            print("12:  Ingresar bid")
            print("13:  Ingresar ask")
            print("14:  Upgrade a Investor")
        while invalido:
            opcion = input("Ingrese su numero de opcion a seguir: ")
            if int(opcion) not in range(1,15):
                pass
            else:
                if isinstance(usuario_actual, Underaged):
                    if int(opcion) in range(1,9):
                        invalido = False
                else:
                    invalido = False

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

    def determinar_match(self, usuario_actual, order_realizada):  # se ejecuta siempre despues de realizar un bid o ask
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
                order_realizada.moneda_de_cambio = mejor_opcion.moneda_de_cambio
                mercado.asks_activos.remove(order_realizada)
                mercado.bids_activos.remove(mejor_opcion)
                order_realizada.ejecutada = True
                mejor_opcion.ejecutada = True
                resto = d(mejor_opcion.divisa_compra) - d(order_realizada.divisa_venta)
                if resto != 0:
                    new_bid = Bid(mejor_opcion.usuario, mercado, str(resto), mejor_opcion.moneda_de_cambio,
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
                new_ask = Ask(order_realizada.usuario, mercado, str(resto), order_realizada.moneda_de_cambio,
                              order_realizada.tiempo)
                maximo = self.maximo_id()
                new_ask.id = str(maximo + 1)
                self.lista_orders.append(new_ask)
                mercado.asks_activos.append(new_ask)
                mercado.orders.append(new_ask)
                order_realizada.divisa_venta = d(order_realizada.divisa_venta) - d(resto)
                order_realizada.moneda_de_cambio = mejor_opcion.moneda_de_cambio
            if still_left:
                self.determinar_match(usuario_actual, new_ask)
            mejor_opcion.match_time = strftime("%Y-%m-%d", gmtime())
            order_realizada.match_time = strftime("%Y-%m-%d", gmtime())
            new_match = Match(order_realizada, mejor_opcion, order_realizada.tiempo)
            self.lista_match.append(new_match)
            return
        elif isinstance(order_realizada, Bid):  # en caso de que se ponga un Bid
            opciones_asks = []  # bids que le convienen a la compra
            for ask in asks:
                if ask.moneda_de_cambio <= order_realizada.moneda_de_cambio:
                    opciones_asks.append(ask)
            if len(opciones_asks) == 0:  # no hay match
                return
            opciones_asks.sort(key=lambda elem: float(elem.moneda_de_cambio), reverse = False)
            mejores_opciones = [opciones_asks.pop(0)]
            for ask in opciones_asks:
                if ask.moneda_de_cambio == mejores_opciones[0].moneda_de_cambio:
                    mejores_opciones.append(ask)
            if len(mejores_opciones) == 1:
                mejor_opcion = mejores_opciones[0]
            elif len(mejores_opciones) > 1:
                mejores_opciones.sort(key=lambda elem: (int(elem.año), int(elem.mes), int(elem.dia)))
                mejor_opcion = mejores_opciones[0]
            divisa_compraventa = mercado.divisa_compraventa  # simbolo
            moneda_de_cambio = mercado.moneda_de_cambio  # simbolo
            if d(order_realizada.divisa_compra) <= d(mejor_opcion.divisa_venta):
                still_left = False
                usuario_actual.balance_currencies[divisa_compraventa] += d(order_realizada.divisa_compra)
                usuario_actual.balance_currencies[moneda_de_cambio] -= (d(order_realizada.divisa_compra)
                                                                        * d(mejor_opcion.moneda_de_cambio))
                mejor_opcion.usuario.balance_currencies[moneda_de_cambio] += (d(order_realizada.divisa_compra)
                                                                                * d(mejor_opcion.moneda_de_cambio))
                mejor_opcion.usuario.balance_currencies[divisa_compraventa] -= d(order_realizada.divisa_compra)
                order_realizada.moneda_de_cambio = mejor_opcion.moneda_de_cambio
                mercado.asks_activos.remove(mejor_opcion)
                mercado.bids_activos.remove(order_realizada)
                order_realizada.ejecutada = True
                mejor_opcion.ejecutada = True
                resto = d(mejor_opcion.divisa_venta) - d(order_realizada.divisa_compra)
                if resto != 0:
                    new_ask = Ask(mejor_opcion.usuario, mercado, str(resto), mejor_opcion.moneda_de_cambio,
                                  mejor_opcion.tiempo)
                    maximo = self.maximo_id()
                    new_ask.id = str(maximo + 1)
                    self.lista_orders.append(new_ask)
                    mercado.asks_activos.append(new_ask)
                    mercado.asks.append(new_ask)  # quitamos el resto de la order
                    mejor_opcion.divisa_venta = d(mejor_opcion.divisa_venta) - d(resto)
            elif d(order_realizada.divisa_compra) > d(mejor_opcion.divisa_venta):
                usuario_actual.balance_currencies[divisa_compraventa] += d(mejor_opcion.divisa_venta)
                usuario_actual.balance_currencies[moneda_de_cambio] -= (d(mejor_opcion.divisa_venta) *
                                                                        d(mejor_opcion.moneda_de_cambio))
                mejor_opcion.usuario.balance_currencies[divisa_compraventa] -= d(mejor_opcion.divisa_venta)
                mejor_opcion.usuario.balance_currencies[moneda_de_cambio] += (d(mejor_opcion.divisa_venta) *
                                                                              d(mejor_opcion.moneda_de_cambio))
                resto = d(order_realizada.divisa_compra) - d(mejor_opcion.divisa_venta)
                mercado.asks_activos.remove(mejor_opcion)
                mercado.bids_activos.remove(order_realizada)
                order_realizada.ejecutada = True
                mejor_opcion.ejecutada = True
                new_bid = Bid(order_realizada.usuario, mercado, str(resto), order_realizada.moneda_de_cambio,
                              order_realizada.tiempo)
                maximo = self.maximo_id()
                new_bid.id = str(maximo + 1)
                self.lista_orders.append(new_bid)
                mercado.bids_activos.append(new_bid)
                mercado.bids.append(new_bid)
                mercado.orders.append(new_bid)
                order_realizada.divisa_compra = d(order_realizada.divisa_compra) - d(resto)
                order_realizada.moneda_de_cambio = mejor_opcion.moneda_de_cambio

            if still_left:
                self.determinar_match(usuario_actual, new_bid)
            mejor_opcion.match_time = strftime("%Y-%m-%d", gmtime())
            order_realizada.match_time = strftime("%Y-%m-%d", gmtime())
            new_match = Match(mejor_opcion, order_realizada, order_realizada.tiempo)
            self.lista_match.append(new_match)
            return

    def determinar_match_parciales_csv(self):
        lista_orders_ordenada = sorted(self.lista_orders, key=lambda elem: (int(elem.año),int(elem.mes), int(elem.dia)),
                                       reverse = True)
        for order in lista_orders_ordenada:
            if order.ejecutada != True:
                self.determinar_match(order.usuario, order)

    def estado_orders(self, usuario_actual):
        print("Sus orders realizadas hasta el momento son las siguientes:")
        for order in self.lista_orders:
            if order.usuario == usuario_actual:
                if order.ejecutada:
                    print(order, "| Tuvo match el dia", order.match_time)
                else:
                    print(order, "| Aun no tiene match")
