from User import *
from csv_reader import *
from Order import *
from Mercado import Mercado, Moneda
from decimal import Decimal as d
from sistema import Sistema
from os.path import exists


def poblar_sistema(archivo, lista_usuarios, lista_mercados):
    if archivo == "users.csv":
        lista_info_usuarios = read(archivo)
        write_ordenado_users(lista_info_usuarios)
        for info_usuario in lista_info_usuarios:
            if "birthday" not in lista_info_usuarios[0].keys():  # no esta claro si sera birthday o birthdate
                cumpleaños = "birthdate"
            else:
                cumpleaños = "birthday"
            usuario = Usuario(info_usuario["username"], info_usuario["name"], info_usuario["lastname"],
                              info_usuario[cumpleaños])
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
    elif archivo == "Currencies.csv" or archivo == "currencies.csv":  # no esta claro si sera con minuscula o no
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
                        usuario.mercados.append(mercado_order)
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

for mercado in lista_mercados:
    if mercado.asks_activos != [] or mercado.bids_activos != []:
        print("MERCADO:", mercado.ticker)
    for order in mercado.asks_activos:
        print(order)
    for order in mercado.bids_activos:
        print(order)

sistema.determinar_match_parciales_csv()
sistema.start()

#for mercado in lista_mercados:
#    for ask in mercado.asks_activos:
#        print(ask.id)
#    for bid in mercado.bids_activos:
#        print(bid.id)

#for match in sistema.lista_match:
#    print("ask:", match.ask.id,"bid:", match.bid.id, match.ask.divisa_venta, match.bid.divisa_compra, match.ask.moneda_de_cambio)

if not exists("Registros/consultas_saldo.csv"):
    escribir = ["Hora", "username\n"]
    escribir = ", ".join(escribir)
else:
    escribir = ""
with open("Registros/consultas_saldo.csv", "a") as data:
    data.write(escribir)
    for consulta in sistema.consulta_saldo:
        #print(consulta)
        escribir = [consulta["Hora"], consulta["username"]+"\n"]
        escribir = ", ".join(escribir)
        data.write(escribir)


if not exists("Registros/consultas_orders_activas.csv"):
    escribir = ["Hora", "username", "order_id", "mercado", "amount", "price", "tipo\n"]
    escribir = ", ".join(escribir)
else:
    escribir = ""
with open("Registros/consultas_orders_activas.csv", "a") as data:
    data.write(escribir)
    for consulta in sistema.consulta_orders_activas:
        #print(consulta)
        escribir = [consulta["Hora"], consulta["username"], consulta["order_id"], consulta["mercado"],
                    str(consulta["amount"]), str(consulta["price"]), consulta["tipo"] + "\n"]
        escribir = ", ".join(escribir)
        data.write(escribir)
print("\n")

if not exists("Registros/consultas_orders_historicas.csv"):
    escribir = ["Hora", "username", "order_id", "mercado", "amount", "price", "tipo", "ejecutada\n"]
    escribir = ", ".join(escribir)
else:
    escribir = ""
with open("Registros/consultas_orders_historicas.csv", "a") as data:
    data.write(escribir)
    for consulta in sistema.consulta_orders_historicas:
        #print(consulta)
        escribir = [consulta["Hora"], consulta["username"], consulta["order_id"], consulta["mercado"],
                    str(consulta["amount"]), str(consulta["price"]), consulta["tipo"], str(consulta["ejecutada"]) + "\n"]
        escribir = ", ".join(escribir)
        data.write(escribir)

print("\n")

if not exists("Registros/consultas_orders_propias.csv"):
    escribir = ["Hora", "username\n"]
    escribir = ", ".join(escribir)
else:
    escribir = ""
with open("Registros/consultas_orders_propias.csv", "a") as data:
    data.write(escribir)
    for consulta in sistema.consulta_orders_propias:
        #print(consulta)
        escribir = [consulta["Hora"], consulta["username"]+"\n"]
        escribir = ", ".join(escribir)
        data.write(escribir)

print("\n")

if not exists("Registros/orders_realizadas.csv"):
    escribir = ["Hora", "username", "order_id", "mercado", "amount", "price", "tipo\n"]
    escribir = ", ".join(escribir)
else:
    escribir = ""
with open("Registros/orders_realizadas.csv", "a") as data:
    data.write(escribir)
    for consulta in sistema.realiza_order:
        #print(consulta)
        escribir = [consulta["Hora"], consulta["username"], consulta["order_id"], consulta["mercado"],
                    str(consulta["amount"]), str(consulta["price"]), consulta["tipo"] + "\n"]
        escribir = ", ".join(escribir)
        data.write(escribir)
print("\n")

if not exists("Registros/match_realizados.csv"):
    escribir = ["Hora", "ask_id", "bid_id", "mercado", "amount", "price\n"]
    escribir = ", ".join(escribir)
else:
    escribir = ""
with open("Registros/match_realizados.csv", "a") as data:
    data.write(escribir)
    for consulta in sistema.realiza_match:
        #print(consulta)
        escribir = [consulta["Hora"], consulta["ask_id"], consulta["bid_id"], consulta["mercado"],
                    str(consulta["amount"]), str(consulta["price"]) + "\n"]
        escribir = ", ".join(escribir)
        data.write(escribir)
print("\n")

for usuario in sistema.lista_usuarios:
    usuario.orders_realizadas = set(usuario.orders_realizadas)
    for order in sistema.lista_orders:
        if order.usuario == usuario:
            usuario.orders_realizadas.add(order.id)

# Escribir bases de datos


with open("users_ordenados.csv", "w") as data:
    data.write("username: string;name: string;lastname: string;birthday: string;orders: list\n")
    for usuario in sistema.lista_usuarios:
        orders = ":".join(usuario.orders_realizadas)
        escribir = (usuario.username, usuario.nombre, usuario.apellido, usuario.nacimiento, orders + "\n")
        escribir = ";".join(escribir)
        data.write(escribir)

with open("orders_ordenadas.csv", "w") as data:
    data.write("order_id: int;ticker: string;amount: float;price: float;type: string;"
               "date_created: string;date_match: string")
    for order in sistema.lista_orders:
        escribir = (order.id, order.mercado.ticker)
        
