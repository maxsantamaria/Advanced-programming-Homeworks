from User import *
from csv_reader import read, write_ordenado
from Order import *
from Mercado import Mercado, Moneda
from decimal import Decimal as d
import datetime as DT

class Sistema:
    def __init__(self, lista_usuarios, lista_mercados, lista_orders, lista_monedas, lista_match):
        self.lista_usuarios = lista_usuarios
        self.lista_mercados = lista_mercados
        self.lista_orders = lista_orders
        self.lista_monedas = lista_monedas
        self.lista_match = lista_match
        # registros de comportamiento de los usuarios
        self.consulta_saldo = []  # lista de diccionarios
        self.consulta_orders_propias = []
        self.consulta_orders_activas = []
        self.consulta_orders_historicas = []
        self.realiza_order = []
        self.realiza_match = []

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
                while True:
                    mercado_a_registrar = input("Ingrese el ticker del mercado al que se quiere registrar: ")
                    for mercado in self.lista_mercados:
                        if mercado_a_registrar == mercado.ticker and mercado not in usuario_actual.mercados:
                            mercado_a_registrar = mercado
                            break
                    if isinstance(mercado_a_registrar, Mercado):
                        break
                    else:
                        print("Nombre de mercado invalido.")
                usuario_actual.agregar_mercado(mercado_a_registrar)
            elif opcion == "4":
                print("1 : Informacion de todos los mercados")
                print("2 : Informacion de un mercado en especifico")
                while True:  # manejo de errores
                    opcion = input("Ingrese una de las 2 opciones: ")
                    if opcion != "1" and opcion != "2":
                        print("Opcion invalida")
                    else:
                        break
                if opcion == "1":
                    for mercado in self.lista_mercados:
                        mercado.desplegar_informacion()
                elif opcion == "2":
                    while True:  # manejo de errores
                        mercado_elegido = input("Ingrese el ticker del mercado especifico: ")
                        for mercado in self.lista_mercados:
                            if mercado.ticker == mercado_elegido:
                                mercado_elegido = mercado
                                break
                        if isinstance(mercado_elegido, Mercado):  # manejo de errores
                            break
                        else:
                            print("Mercado invalido.")
                    mercado_elegido.desplegar_informacion()
            elif opcion == "5":
                for mercado in self.lista_mercados:
                    if mercado.asks_activos != [] or mercado.bids_activos != []:
                        print("MERCADO:", mercado.ticker)
                    for order in mercado.asks_activos:
                        self.consulta_orders_activas.append({"username" : usuario_actual.username,
                                                             "order_id" : order.id,
                                                             "price"    : order.moneda_de_cambio,
                                                             "mercado"  : mercado.ticker,
                                                             "ejecutada": order.ejecutada,
                                                             "Hora"     : strftime("%H:%M")})

                        self.consulta_orders_activas[-1].update({"tipo"   : "ask",
                                                                 "amount" : order.divisa_venta})
                        print(order)
                    for order in mercado.bids_activos:
                        self.consulta_orders_activas.append({"username"  : usuario_actual.username,
                                                             "order_id"  : order.id,
                                                             "price"     : order.moneda_de_cambio,
                                                             "mercado"   : mercado.ticker,
                                                             "ejecutada" : order.ejecutada,
                                                             "Hora"      : strftime("%H:%M")})
                        self.consulta_orders_activas[-1].update({"tipo"   : "bid",
                                                                    "amount" : order.divisa_compra})
                        print(order)
            elif opcion == "6":
                self.consulta_saldo.append({"username" : usuario_actual.username, "Hora" : strftime("%H:%M")})
                print("Su saldo es el siguiente:")
                for symbol, saldo in usuario_actual.balance_currencies.items():
                    print(symbol, saldo)
            elif opcion == "7":
                print("Has cerrado sesión. \n")
                usuario_actual = identificarse(self.lista_usuarios)
                self.estado_orders(usuario_actual)

            elif opcion == "9":
                print("1: Informacion de todos los usuarios\n2: Historial de matches\n3: Informacion de monedas")
                while True:  # manejo de errores
                    opcion_consulta = input("Ingrese la opcion de la consulta a realizar: ")
                    if opcion_consulta != "1" and opcion_consulta != "2" and opcion_consulta != "3":
                        print("Opcion invalida")  # manejo de errores
                    else:
                        break
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
                    while True:  # manejo de errores
                        moneda_elegida = input("Ingresa uno de los simbolos de la lista anterior de monedas: ")
                        monedas_con_mismo_simbolo = list(filter(lambda x : x.simbolo == moneda_elegida,
                                                                self.lista_monedas))
                        if len(monedas_con_mismo_simbolo) > 0:  # hay monedas igual a la elegida
                            print(monedas_con_mismo_simbolo[0])
                            break
                        else:
                            print("Simbolo de moneda invalido")
                    mercados_activos = 0
                    mercados_con_la_moneda = []
                    for mercado in self.lista_mercados:
                        if len(mercado.asks_activos) != 0 or len(mercado.bids_activos) != 0:
                            if (mercado.divisa_compraventa == moneda_elegida or
                                        mercado.moneda_de_cambio == moneda_elegida):
                                mercados_activos += 1
                                mercados_con_la_moneda.append(mercado)
                    print("Hay " + str(mercados_activos) + " mercados con orders activas de", moneda_elegida)
                    for mercado in mercados_con_la_moneda:
                        match_en_mercado = []
                        for match in self.lista_match:
                            if match.ask.mercado == mercado:
                                match_en_mercado.append(match)
                        print("-"*10, "Mercado: ", mercado.ticker, "-" * 10)
                        orders_mercado = sorted(mercado.orders, key=lambda elem: (int(elem.año),int(elem.mes),
                                                                                  int(elem.dia)), reverse = True)
                        print("-Ultima order: ", orders_mercado[0])
                        if match_en_mercado != []:
                            match_en_mercado.sort(key=lambda elem: (int(elem.año),int(elem.mes), int(elem.dia)),
                                                  reverse = True)
                            ultimo_match = match_en_mercado[0]
                            print("-Precio actual de", mercado.divisa_compraventa, ":",
                                  ultimo_match.bid.moneda_de_cambio, mercado.moneda_de_cambio)
                            print("    Ultimo match -> ", ultimo_match.tiempo)
            elif opcion == "10":
                print("1: Desplegar orders en una fecha especifica\n2: Desplegar orders entre 2 fechas\n"
                      "3: Desplegar orders en un mercado especifico")
                while True:
                    opcion_desplegar_orders = input("Ingrese una de las opciones (1, 2 o 3): ")
                    if opcion_desplegar_orders != "1" and opcion_desplegar_orders != "2" \
                            and opcion_desplegar_orders != "3":
                        print("Opcion invalida")  # manejo de errores
                    else:
                        break
                if opcion_desplegar_orders == "1":
                    valido = False
                    while not valido:
                        fecha1 = input("Ingrese la fecha especifica (YYYY-MM-DD): ")
                        valido = self.fecha_limite(fecha1, usuario_actual)
                        if not valido:
                            print("No puedes ver registro de orders antes de los últimos 7 días. "
                                  "Para hacerlo debes ser Investor")
                    fecha2 = ""
                    impresiones = []
                    for order in self.lista_orders:
                        imprimio = order.desplegar_order_por_fecha(fecha1, fecha2)
                        impresiones.append(imprimio)
                    if True not in impresiones:
                        print("No hay orders en la fecha indicada.")
                elif opcion_desplegar_orders == "2":
                    valido1 = False
                    valido2 = False
                    while not valido1 or not valido2:
                        fecha1 = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                        fecha2 = input("Ingrese la fecha final (YYYY-MM-DD): ")
                        valido1 = self.fecha_limite(fecha1, usuario_actual)
                        valido2 = self.fecha_limite(fecha2, usuario_actual)
                        if not valido1 or not valido2:
                            print("No cumple los requisitos. Ingresa otra vez.")
                    impresiones = []
                    for order in self.lista_orders:
                        imprimio = order.desplegar_order_por_fecha(fecha1, fecha2)
                        impresiones.append(imprimio)
                    if True not in impresiones:
                        print("No hay orders en la fecha indicada.")
                elif opcion_desplegar_orders == "3":
                    mercado_a_desplegar = input("Ingrese el ticker del mercado a observar: ")
                    for mercado in self.lista_mercados:
                        if mercado_a_desplegar == mercado.ticker:
                            mercado_a_desplegar = mercado
                            break
                    impresiones = []
                    for order in self.lista_orders:
                        valido = self.fecha_limite(order.tiempo, usuario_actual)
                        if valido:
                            imprimio = order.desplegar_order_por_mercado(mercado_a_desplegar)
                            if imprimio:
                                self.consulta_orders_historicas.append({"username": usuario_actual.username,
                                                                        "order_id": order.id,
                                                                        "price": order.moneda_de_cambio,
                                                                        "mercado": mercado_a_desplegar.ticker,
                                                                        "ejecutada": order.ejecutada,
                                                                        "Hora" : strftime("%H:%M")})
                                if isinstance(order, Ask):
                                    self.consulta_orders_historicas[-1].update({"tipo": "ask",
                                                                                "amount": order.divisa_venta})
                                elif isinstance(order, Bid):
                                    self.consulta_orders_historicas[-1].update({"tipo": "bid",
                                                                                "amount": order.divisa_compra})
                            impresiones.append(imprimio)
                    if True not in impresiones:  # manejo de errores
                        print("No hay orders en el mercado indicado.")

            elif opcion == "11":
                while True:
                    usuario_destino = input("Ingresa el nombre de usuario del destinatario: ")

                    for usuario in self.lista_usuarios:
                        if usuario.username == usuario_destino and usuario.username != usuario_actual.username:
                            usuario_destino = usuario
                            break

                    if isinstance(usuario_destino, Trader):
                        break
                    elif isinstance(usuario_destino, Underaged):
                        print("No puedes transferirle a un usuario Underaged")
                    else:
                        print("Usuario no valido.")
                print(usuario_destino.balance_currencies)
                simbolo_invalido = True  # manejo de errores
                cantidad_invalido = True  # manejo de errores
                while cantidad_invalido or simbolo_invalido:
                    monto = input("Ingresa el monto a transferir (ej.: 100 DCC): ")
                    numero = True
                    cantidad = ""
                    simbolo = ""
                    monto = monto.strip()
                    for letra in monto:
                        if numero and letra != " ":
                            cantidad += letra
                        elif not numero:
                            simbolo += letra
                        if letra == " ":
                            numero = False
                    simbolo = simbolo.strip()
                    cantidad = cantidad.strip()
                    try:  # manejo de errores
                        float(cantidad)
                    except:
                        print("Cantidad no valida")
                    else:
                        cantidad_invalido = False
                    for moneda in self.lista_monedas:  # manejo de errores
                        if moneda.simbolo == simbolo:
                            simbolo_invalido = False
                    if simbolo_invalido:
                        print("Simbolo de moneda invalido")
                for mercado in self.lista_mercados:
                    if mercado.divisa_compraventa == simbolo:
                        mercado_comision = mercado
                        break
                usuario_actual.transferir_dinero(cantidad, usuario_destino, mercado_comision)
                print(usuario_destino.balance_currencies)
            elif opcion == "12":
                volver = False  # para volver al menu
                cantidad_match_antes = len(self.lista_match)
                while True:  # se hace este while para poder usar el break despues y que no corra el if completo
                    while True:  # manejo de errores
                        mercado_actual = input("Ingrese el ticker del mercado para hacer un bid: ")
                        for mercado in self.lista_mercados:
                            if mercado.ticker == mercado_actual:
                                mercado_actual = mercado
                                break
                        if isinstance(mercado_actual, Mercado):
                            break
                        else:
                            print("Mercado invalido")
                    if mercado_actual not in usuario_actual.mercados:
                        print("No estas registrado en ese mercado. Debes hacer eso primero")
                        break
                    divisa_compraventa = mercado_actual.divisa_compraventa
                    moneda_de_cambio = mercado_actual.moneda_de_cambio
                    conteo_orders_dia = 0
                    conteo_orders_activas = 0
                    tiempo_actual = strftime("%Y-%m-%d", gmtime())
                    for order in self.lista_orders:
                        if order.usuario == usuario_actual:
                            if order.tiempo == tiempo_actual:
                                conteo_orders_dia += 1
                            if not order.ejecutada:
                                conteo_orders_activas
                    if conteo_orders_dia >= 15 :  # limite de orders para Trader
                        if not isinstance(usuario_actual, Investor):
                            print("No puedes hacer mas de 15 orders en un dia")
                            break
                    if conteo_orders_activas >= 5:
                        if not isinstance(usuario_actual, Investor):
                            print("No puedes tener mas de 5 orders activas")
                            break
                    while True:
                        divisa_compra = input("Ingrese la cantidad de " + mercado_actual.ticker[0:3] +
                                              " que quieres comprar (0 para volver al menu): ")
                        moneda_de_cambio = input("Ingrese el precio en " + mercado_actual.ticker[3:] +
                                                 " al que compras una unidad (0 para volver al menu): ")
                        if divisa_compra == "0" or moneda_de_cambio == "0":
                            volver = True
                            break
                        try:
                            float(divisa_compra)
                            float(moneda_de_cambio)
                        except:
                            print("Formato incorrecto de ingreso. Recuerda solo ingresar el numero de lo pedido.")
                        else:
                            pago = d(divisa_compra) * d(moneda_de_cambio)
                            balance_real = usuario_actual.balance_currencies[mercado_actual.moneda_de_cambio]
                            # balance real va a considerar las orders activas del usuario en el mercado, para que
                            # no ingrese mas dinero del que puede pagar
                            for order in self.lista_orders:
                                if (order.mercado.divisa_compraventa == mercado_actual.divisa_compraventa and
                                            order.ejecutada == False and order.usuario == usuario_actual):
                                    if isinstance(order, Ask):
                                        balance_real -= d(order.divisa_venta)
                                    elif isinstance(order, Bid):
                                        balance_real -= d(order.divisa_compra) * d(order.moneda_de_cambio)
                                elif (order.mercado.moneda_de_cambio == mercado_actual.moneda_de_cambio and
                                              order.ejecutada == False and order.usuario == usuario_actual):
                                    if isinstance(order, Ask):
                                        balance_real -= d(order.divisa_venta)
                                    elif isinstance(order, Bid):
                                        balance_real -= d(order.divisa_compra) * d(order.moneda_de_cambio)
                            print(balance_real)
                            if pago > usuario_actual.balance_currencies[mercado_actual.ticker[3:]]:
                                print("No tienes suficiente dinero para hacer esa order")
                            elif pago > balance_real:
                                print("No puedes hacer la order porque tienes mas dinero ingresado en otras.")
                            elif pago < 0 or d(moneda_de_cambio) < 0:
                                print("Debes ingresar un numero positivo.")
                            else:
                                break
                    if volver:
                        break
                    nuevo_bid = usuario_actual.ingresar_bid(usuario_actual, mercado_actual, divisa_compra,
                                                            moneda_de_cambio)
                    maximo = self.maximo_id()
                    nuevo_bid.id = str(maximo + 1)
                    self.realiza_order.append({"username" : usuario_actual.username,
                                               "order_id" : nuevo_bid.id,
                                               "mercado"  : mercado_actual.ticker,
                                               "tipo"     : "bid",
                                               "amount"   : nuevo_bid.divisa_compra,
                                               "price"    : nuevo_bid.moneda_de_cambio,
                                               "Hora"     : strftime("%H:%M")})
                    self.lista_orders.append(nuevo_bid)
                    self.determinar_match(usuario_actual, nuevo_bid)
                    print(usuario_actual.balance_currencies)
                    break
                cantidad_match_despues = len(self.lista_match)
                if cantidad_match_antes < cantidad_match_despues:
                    print("Felicidades! Tu order ha hecho match! Se ha actualizado el saldo con la nueva informacion.")
            elif opcion == "13":
                volver = False  # para volver al menu
                cantidad_match_antes = len(self.lista_match)
                while True:
                    while True:
                        mercado_actual = input("Ingrese el ticker del mercado para hacer un ask: ")
                        for mercado in self.lista_mercados:
                            if mercado.ticker == mercado_actual:
                                mercado_actual = mercado
                                break
                        if isinstance(mercado_actual, Mercado):
                            break
                        else:
                            print("Mercado invalido")
                    if mercado_actual not in usuario_actual.mercados:
                        print("No estas registrado en ese mercado. Debes hacer eso primero")
                        break
                    conteo_orders_dia = 0
                    conteo_orders_activas = 0
                    tiempo_actual = strftime("%Y-%m-%d", gmtime())
                    for order in self.lista_orders:
                        if order.usuario == usuario_actual:
                            if order.tiempo == tiempo_actual:
                                conteo_orders_dia += 1
                            if not order.ejecutada:
                                conteo_orders_activas += 1
                    if conteo_orders_dia >= 15:  # limite de orders para Trader
                        if not isinstance(usuario_actual, Investor):
                            print("No puedes hacer mas de 15 orders en un dia")
                            break
                    if conteo_orders_activas >= 5:
                        if not isinstance(usuario_actual, Investor):
                            print("No puedes tener mas de 5 orders activas")
                            break
                    while True:  # manejo de errores
                        divisa_venta = input("Ingrese la cantidad de " + mercado_actual.ticker[0:3] +
                                             " que quieres vender (0 para volver al menu): ")
                        moneda_de_cambio = input("Ingrese el precio en " + mercado_actual.ticker[3:] +
                                                 " al que vendes una unidad (0 para volver al menu): ")
                        if divisa_venta == "0" or moneda_de_cambio == "0":
                            volver = True
                            break
                        try:
                            float(divisa_venta)
                            float(moneda_de_cambio)
                        except:
                            print("Cantidad invalida ingresada. Recuerda solo ingresar el numero de lo pedido.")
                        else:
                            pago = d(divisa_venta)
                            balance_real = usuario_actual.balance_currencies[mercado_actual.divisa_compraventa]
                            # balance real va a considerar las orders activas del usuario en el mercado, para que
                            # no ingrese mas dinero del que puede pagar
                            for order in self.lista_orders:  # esto se hace para calcular el balance real
                                if (order.mercado.divisa_compraventa == mercado_actual.divisa_compraventa and
                                            order.ejecutada == False and order.usuario == usuario_actual):
                                    if isinstance(order, Ask):
                                        balance_real -= d(order.divisa_venta)
                                    elif isinstance(order, Bid):
                                        balance_real -= d(order.divisa_compra) * d(order.moneda_de_cambio)
                                elif (order.mercado.moneda_de_cambio == mercado_actual.moneda_de_cambio and
                                              order.ejecutada == False and order.usuario == usuario_actual):
                                    if isinstance(order, Ask):
                                        balance_real -= d(order.divisa_venta)
                                    elif isinstance(order, Bid):
                                        balance_real -= d(order.divisa_compra) * d(order.moneda_de_cambio)
                            if pago > usuario_actual.balance_currencies[mercado_actual.divisa_compraventa]:
                                print("No tienes el dinero suficiente para hacer la order")
                            elif pago > balance_real:
                                print("No puedes hacer la order porque tienes mas dinero ingresado en otras.")
                            elif pago < 0 or int(moneda_de_cambio) <= 0:
                                print("Debes ingresar un numero positivo.")
                            else:
                                break
                    if volver:
                        break
                    nuevo_ask = usuario_actual.ingresar_ask(usuario_actual, mercado_actual, divisa_venta,
                                                            moneda_de_cambio)
                    maximo = self.maximo_id()
                    nuevo_ask.id = str(maximo + 1)
                    self.realiza_order.append({"username" : usuario_actual.username,
                                               "order_id" : nuevo_ask.id,
                                               "mercado"  : mercado_actual.ticker,
                                               "tipo"     : "ask",
                                               "amount"   : nuevo_ask.divisa_venta,
                                               "price"    : nuevo_ask.moneda_de_cambio,
                                               "Hora"     : strftime("%H:%M")})
                    self.lista_orders.append(nuevo_ask)
                    self.determinar_match(usuario_actual, nuevo_ask)
                    print(usuario_actual.balance_currencies)
                    break
                cantidad_match_despues = len(self.lista_match)
                if cantidad_match_antes < cantidad_match_despues:
                    print("Felicidades! Tu order ha hecho match! Se ha actualizado el saldo con la nueva informacion.")
            elif opcion == "14":  # upgrade
                usuario_actual = self.upgrade(usuario_actual)

            elif opcion == "15":
                self.consulta_orders_propias.append({"username" : usuario_actual.username, "Hora" : strftime("%H:%M")})
                self.estado_orders(usuario_actual)
            elif opcion == "16":
                while True:
                    id_eliminar = input("Ingresa el ID de la order que quieres eliminar (tiene que ser tuya!): ")
                    try:  # manejo de errores
                        int(id_eliminar)
                    except:
                        print("ID no valido")
                    else:
                        if int(id_eliminar) not in range(1, int(self.maximo_id()) + 1):
                            print("No existe la order")
                        else:
                            break

                for order in self.lista_orders:
                    if order.id == id_eliminar:
                        order_eliminar = order
                if order_eliminar.usuario == usuario_actual:
                    if not order_eliminar.ejecutada:
                        for mercado in self.lista_mercados:
                            if mercado == order_eliminar.mercado:
                                mercado.orders.remove(order_eliminar)
                                if isinstance(order_eliminar, Ask):
                                    mercado.asks_activos.remove(order_eliminar)
                                elif isinstance(order_eliminar, Bid):
                                    mercado.bids_activos.remove(order_eliminar)
                        self.lista_orders.remove(order_eliminar)
                        del order_eliminar
                    else:
                        print("No puedes eliminar una order ya ejecutada")
                else:
                    print("Esta order no te pertenece")

            input("Presiona enter para continuar  ")

    def fecha_limite(self, fecha_indicada, usuario_actual):  # para determinar si la fecha esta en el rango
        try:
            año_indicado = int(fecha_indicada[0:4])
            mes_indicado = int(fecha_indicada[5:7])
            dia_indicado = int(fecha_indicada[8:])
            if fecha_indicada > strftime("%Y-%m-%d") or mes_indicado > 12 or dia_indicado > 31:
                print("Fecha invalida")  # manejo de errores
                return False
            week_ago = str(DT.date.today() - DT.timedelta(days=7))
            if isinstance(usuario_actual, Investor):  # investor no tienen restriccion
                return True
            if fecha_indicada > week_ago:
                return True
            return False
        except:
            print("Formato no valido")
            return False

    def upgrade(self, usuario_actual):
        if isinstance(usuario_actual, Investor):
            print("Ya eres Investor")
            return usuario_actual
        if usuario_actual.balance_currencies["DCC"] < d("300000"):
            print("No tienes dinero suficiente para hacer un upgrade a Investor.")
            return usuario_actual
        while True:  # manejo de errores
            seguro = input("Estas seguro de que quieres pasar a ser Investor (si/no): ")
            if seguro == "si":
                nuevo_usuario = Investor(usuario_actual.username, usuario_actual.nombre, usuario_actual.apellido,
                                         usuario_actual.nacimiento)
                nuevo_usuario.balance_currencies = usuario_actual.balance_currencies
                nuevo_usuario.balance_currencies["DCC"] -= d("300000")
                nuevo_usuario.mercados = usuario_actual.mercados
                for order in self.lista_orders:
                    if order.usuario == usuario_actual:
                        order.usuario = nuevo_usuario
                self.lista_usuarios.remove(usuario_actual)
                del usuario_actual
                self.lista_usuarios.append(nuevo_usuario)
                return nuevo_usuario
                break
            elif seguro == "no":
                return usuario_actual
                break
            else:
                print("Opcion invalida")  # manejo de errores




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
            print("10:  Lista de orders sistema")
            print("11:  Banco")
            print("12:  Ingresar bid")
            print("13:  Ingresar ask")
            print("14:  Upgrade a Investor")
            print("15:  Estado de orders propias")
            print("16:  Cancelar una order activa")
        while invalido:
            opcion = input("Ingrese su numero de opcion a seguir: ")
            try:
                o = int(opcion)
            except:
                pass
            else:
                if int(opcion) not in range(1, 17):
                    pass
                else:
                    if isinstance(usuario_actual, Underaged):
                        if int(opcion) in range(1, 10):
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
            print("")  # salto de linea

    def se_hizo_despues(self, order_realizada, otra_order):  # se usa para ver si la order realizada se hizo despues (T)
        if int(order_realizada.año) > int(otra_order.año):  # o antes (F) que la otra order
            return True
        elif int(order_realizada.año) < int(otra_order.año):
            return False
        else:
            if int(order_realizada.mes) > int(otra_order.mes):
                return True
            elif int(order_realizada.mes) < int(otra_order.mes):
                return False
            else:
                if int(order_realizada.dia) >= int(otra_order.dia):
                    return True
                else:
                    return False

    def determinar_match(self, usuario_actual, order_realizada):  # se ejecuta siempre despues de realizar un bid o ask
        mercado = order_realizada.mercado
        asks = []
        bids = []
        for order in self.lista_orders:
            if (order.mercado == mercado and order != order_realizada and order.ejecutada == False and
                        order.usuario != usuario_actual):
                valido = self.se_hizo_despues(order_realizada, order)
                print(valido, "order ingresada", order_realizada.id, "order comparacion", order.id)
                if isinstance(order, Ask) and valido:
                    asks.append(order)
                elif isinstance(order, Bid) and valido:
                    bids.append(order)
        still_left = True  # variable que es False cuando ya no hay mas match posible con la order realizada
        #while still_left:

        if isinstance(order_realizada, Ask):  # en caso de que se ponga un Ask
            opciones_bids = []  # bids que le convienen a la compra
            for bid in bids:
                if d(bid.moneda_de_cambio) >= d(order_realizada.moneda_de_cambio):
                    opciones_bids.append(bid)
            if len(opciones_bids) == 0:  # no hay match
                return
            opciones_bids.sort(key=lambda elem: float(elem.moneda_de_cambio), reverse = True)
            mejores_opciones = [opciones_bids.pop(0)]
            for bid in opciones_bids:
                if bid.moneda_de_cambio == mejores_opciones[0].moneda_de_cambio:
                    mejores_opciones.append(bid)
            if len(mejores_opciones) == 1:  # prioridad mejor precio
                mejor_opcion = mejores_opciones[0]
            elif len(mejores_opciones) > 1:
                investors = []  # prioridad investor
                for opcion in mejores_opciones:
                    if isinstance(opcion.usuario, Investor):
                        mejor_opcion = opcion
                        investors.append(opcion)
                if len(investors) == 1:
                    pass
                elif len(investors) > 1:
                    investors.sort(key=lambda elem: (int(elem.año), int(elem.mes), int(elem.dia)))  # prioridad tiempo
                    mejor_opcion = investors[0]
                else:
                    mejores_opciones.sort(key=lambda elem: (int(elem.año), int(elem.mes), int(elem.dia)))
                    mejor_opcion = mejores_opciones[0]  # prioridad tiempo


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
                    self.realiza_order.append({"username" : usuario_actual.username,
                                               "order_id" : new_bid.id,
                                               "mercado"  : mercado.ticker,
                                               "tipo"     : "bid",
                                               "amount"   : new_bid.divisa_compra,
                                               "price"    : new_bid.moneda_de_cambio,
                                               "Hora"     : strftime("%H:%M")})
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
            self.realiza_match.append({"ask_id" : new_match.ask.id, "bid_id" : new_match.bid.id,
                                       "amount" : new_match.ask.divisa_venta, "price" : new_match.bid.moneda_de_cambio,
                                       "Hora" : strftime("%H:%M"), "mercado" : new_match.ask.mercado.ticker})
            self.lista_match.append(new_match)
            return
        elif isinstance(order_realizada, Bid):  # en caso de que se ponga un Bid
            opciones_asks = []  # asks que le convienen a la compra
            for ask in asks:
                if d(ask.moneda_de_cambio) <= d(order_realizada.moneda_de_cambio):
                    opciones_asks.append(ask)
            if usuario_actual.username == "ofvera":
                for opcion in opciones_asks:
                    print(opcion.id)
            if len(opciones_asks) == 0:  # no hay match
                return
            opciones_asks.sort(key=lambda elem: float(elem.moneda_de_cambio), reverse = False)
            mejores_opciones = [opciones_asks.pop(0)]
            for ask in opciones_asks:
                if ask.moneda_de_cambio == mejores_opciones[0].moneda_de_cambio:
                    mejores_opciones.append(ask)
            if len(mejores_opciones) == 1:  # prioridad mejor precio
                mejor_opcion = mejores_opciones[0]
            elif len(mejores_opciones) > 1:
                investors = []  # prioridad investor
                for opcion in mejores_opciones:
                    if isinstance(opcion.usuario, Investor):
                        mejor_opcion = opcion
                        investors.append(opcion)
                if len(investors) == 1:
                    pass
                elif len(investors) > 1:
                    investors.sort(key=lambda elem: (int(elem.año), int(elem.mes), int(elem.dia)))  # prioridad tiempo
                    mejor_opcion = investors[0]
                else:
                    mejores_opciones.sort(key=lambda elem: (int(elem.año), int(elem.mes), int(elem.dia)))
                    mejor_opcion = mejores_opciones[0]  # prioridad tiempo
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
                    self.realiza_order.append({"username" : usuario_actual.username,
                                               "order_id" : new_ask.id,
                                               "mercado"  : mercado.ticker,
                                               "tipo"     : "bid",
                                               "amount"   : new_ask.divisa_venta,
                                               "price"    : new_ask.moneda_de_cambio,
                                               "Hora"     : strftime("%H:%M")})
                    self.lista_orders.append(new_ask)
                    mercado.orders.append(new_ask)
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
            self.realiza_match.append({"ask_id": new_match.ask.id, "bid_id": new_match.bid.id,
                                       "amount": new_match.ask.divisa_venta, "price": new_match.bid.moneda_de_cambio,
                                       "Hora": strftime("%H:%M"), "mercado": new_match.ask.mercado.ticker})
            self.lista_match.append(new_match)
            return

    def determinar_match_parciales_csv(self):
        lista_orders_ordenada = sorted(self.lista_orders, key=lambda elem: (int(elem.año),int(elem.mes), int(elem.dia)),
                                       reverse = False)
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
        print("")  # salto de linea
