class Order:
    def __init__(self, usuario, mercado, tiempo):
        self.usuario = usuario
        self.mercado = mercado
        self.ejecutada = False
        self.match_time = ""
        self.id = ""
        self.tiempo = tiempo
        self.año = tiempo[0:4]
        self.mes = tiempo[5:7]
        self.dia = tiempo[8:]

    def desplegar_order_por_fecha(self, fecha1, fecha2):
        imprimir = ("Order ID: " + self.id + " | " + self.tiempo + " | En mercado " + self.mercado.ticker
                    + " | Usuario: " + self.usuario.username)
        cumple_condicion = False
        if fecha2 == "":
            if self.tiempo == fecha1:
                cumple_condicion = True
        elif fecha2 != "":
            año = self.tiempo[0:4]
            mes = self.tiempo[5:7]
            dia = self.tiempo[8:]
            año_comienzo = fecha1[0:4]
            mes_comienzo = fecha1[5:7]
            dia_comienzo = fecha1[8:]
            año_final = fecha2[0:4]
            mes_final = fecha2[5:7]
            dia_final = fecha2[8:]
            if año > año_comienzo:
                if año < año_final:
                    cumple_condicion = True
                elif año == año_final and mes < mes_final:
                    cumple_condicion = True
                elif año == año_final and mes == mes_final and dia <= dia_final:
                    cumple_condicion = True
            elif año == año_comienzo:
                if mes > mes_comienzo:
                    cumple_condicion = True
                elif mes == mes_comienzo and dia >= dia_comienzo:
                    cumple_condicion = True
        if cumple_condicion:
            return imprimir
        else:
            return ""
    def desplegar_order_por_mercado(self, mercado):
        imprimir = ("Order ID: " + self.id + " | " + self.tiempo + " | En mercado " + self.mercado.ticker
                    + " | Usuario: " + self.usuario.username)
        if self.mercado.ticker == mercado.ticker:
            return imprimir
        else:
            return ""
    def __str__(self):
        imprimir = ("Order ID: " + self.id + " | " + self.tiempo + " | En mercado " + self.mercado.ticker
                    + " | Usuario: " + self.usuario.username)
        return imprimir

class Ask(Order):
    def __init__(self, usuario, mercado, divisa_venta, moneda_de_cambio, tiempo):
        Order.__init__(self, usuario, mercado, tiempo)
        self.divisa_venta = divisa_venta  # son cantidades
        self.moneda_de_cambio = moneda_de_cambio  # son cantidades

    def desplegar_order_por_fecha(self, fecha1, fecha2):
        imprimir1 = super().desplegar_order_por_fecha(fecha1, fecha2)
        simbolo1 = self.mercado.ticker[0:3]
        simbolo2 = self.mercado.ticker[3:]
        imprimir2 = (" | " + "ASK de " + str(self.divisa_venta) + simbolo1 + " a cambio de " +
                     str(self.moneda_de_cambio) + simbolo2)
        if imprimir1 != "":
            print(imprimir1 + imprimir2, end = " ")
            if self.ejecutada:
                print("| Tuvo match el dia", self.match_time)
            else:
                print("| Aun no tiene match")
            return True  # para comprobar que se imprimio algo
        return False  # para comprobar que no se imprimio nada

    def desplegar_order_por_mercado(self, mercado_especifico):
        imprimir1 = super().desplegar_order_por_mercado(mercado_especifico)
        simbolo1 = self.mercado.ticker[0:3]
        simbolo2 = self.mercado.ticker[3:]
        imprimir2 = (" | " + "ASK de " + str(self.divisa_venta) + simbolo1 + " a cambio de " +
                     str(self.moneda_de_cambio) + simbolo2)

        if imprimir1 != "":
            print(imprimir1 + imprimir2, end = " ")
            if self.ejecutada:
                print("| Tuvo match el dia", self.match_time)
            else:
                print("| Aun no tiene match")

            return True
        return False

    def __str__(self):
        imprimir1 = super().__str__()
        simbolo1 = self.mercado.ticker[0:3]
        simbolo2 = self.mercado.ticker[3:]
        imprimir2 = (" | " + "ASK de " + str(self.divisa_venta) + simbolo1 + " a cambio de " +
                     str(self.moneda_de_cambio) + simbolo2)
        return imprimir1 + imprimir2

class Bid(Order):
    def __init__(self, usuario, mercado, divisa_compra, moneda_de_cambio, tiempo):
        Order.__init__(self, usuario, mercado, tiempo)
        self.divisa_compra = divisa_compra  # son cantidades
        self.moneda_de_cambio = moneda_de_cambio  # son cantidades

    def desplegar_order_por_fecha(self, fecha1, fecha2):
        imprimir1 = super().desplegar_order_por_fecha(fecha1, fecha2)
        simbolo1 = self.mercado.ticker[0:3]
        simbolo2 = self.mercado.ticker[3:]
        imprimir2 = (" | " + "BID de " + str(self.divisa_compra) + simbolo1 + " a cambio de " +
                     str(self.moneda_de_cambio) + simbolo2)
        if imprimir1 != "":
            print(imprimir1 + imprimir2, end = " ")
            if self.ejecutada:
                print("| Tuvo match el dia", self.match_time)
            else:
                print("| Aun no tiene match")
            return True
        return False

    def desplegar_order_por_mercado(self, mercado):
        imprimir1 = super().desplegar_order_por_mercado(mercado)
        simbolo1 = self.mercado.ticker[0:3]
        simbolo2 = self.mercado.ticker[3:]
        imprimir2 = (" | " + "BID de " + str(self.divisa_compra) + simbolo1 + " a cambio de " +
                     str(self.moneda_de_cambio) + simbolo2)
        if imprimir1 != "":
            print(imprimir1 + imprimir2, end = " ")
            if self.ejecutada:
                print("| Tuvo match el dia", self.match_time)
            else:
                print("| Aun no tiene match")
            return True
        return False

    def __str__(self):
        imprimir1 = super().__str__()
        simbolo1 = self.mercado.ticker[0:3]
        simbolo2 = self.mercado.ticker[3:]
        imprimir2 = (" | " + "BID de " + str(self.divisa_compra) + simbolo1 + " a cambio de " +
                     str(self.moneda_de_cambio) + simbolo2)
        return imprimir1 + imprimir2


class Match:
    def __init__(self, ask, bid, tiempo):
        self.ask = ask
        self.bid = bid
        self.tiempo = tiempo
        self.año = tiempo[0:4]
        self.mes = tiempo[5:7]
        self.dia = tiempo[8:]
