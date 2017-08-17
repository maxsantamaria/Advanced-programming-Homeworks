from abc import ABCMeta, abstractmethod
import time

class Producto(metaclass = ABCMeta):
    def __init__(self, nombre, SKU, precio):
        self.nombre = nombre
        self.SKU = SKU
        self.precio = precio

    def __str__(self):
        mensaje = "[" + self.SKU + "] " + self.nombre + " $" + self.precio + "\n"
        return mensaje

class Comida(Producto, metaclass = ABCMeta):
    def __init__(self, nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento):
        super().__init__(nombre, SKU, precio)
        self.calorias = calorias
        self.proteinas = proteinas
        self.carbohidratos = carbohidratos
        self.grasa = grasa
        self.fecha_vencimiento = fecha_vencimiento

    def __str__(self):
        imprimir1 = super().__str__()
        imprimir2 = ("Calorias" + " = " +
                    self.calorias + " (kcal)\n" + "Proteinas" + " = " + self.proteinas + " (g)\n" + "Carbohidratos"
                    + " = " + self.carbohidratos + " (g)\n" + "Grasa" + " = " + self.grasa + " (g)")
        return imprimir1 + imprimir2

class Lacteo(Comida):
    def __init__(self, nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento, calcio):
        super().__init__(nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento)
        self.calcio = calcio

    def __str__(self):
        imprimir1 = super().__str__()
        imprimir2 = ("\n" + "Calcio"
                    + " = " + self.calcio + " (mg)")
        return imprimir1 + imprimir2

class Verdura(Comida):
    def __init__(self, nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento, vitamina):
        super().__init__(nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento)
        self.vitamina = vitamina

    def __str__(self):
        imprimir = ("Calorias" + " = " +
                    self.calorias + " (kcal)\n" + "Proteinas" + " = " + self.proteinas + " (g)\n" + "Carbohidratos"
                    + " = " + self.carbohidratos + " (g)\n" + "Grasa" + " = " + self.grasa + " (g)\n" + "Vitamina C"
                    + " = " + self.vitamina + " (mg)")
        return imprimir


class Carne(Comida):
    def __init__(self, nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento, tipo):
        super().__init__(nombre, SKU, precio, calorias, proteinas, carbohidratos, grasa, fecha_vencimiento)
        self.tipo = tipo


    def __str__(self):
        imprimir = ("Calorias" + " = " +
                    self.calorias + " (kcal)\n" + "Proteinas" + " = " + self.proteinas + " (g)\n" + "Carbohidratos"
                    + " = " + self.carbohidratos + " (g)\n" + "Grasa" + " = " + self.grasa + " (g)\n" + "Tipo = "
                    + self.tipo)
        return imprimir

class Vestuario(Producto):
    def __init__(self, talla, categoria, nombre, SKU, precio):
        super().__init__(nombre, SKU, precio)
        self.talla = talla
        self.categoria = categoria




class Especial(Comida, Vestuario):
    def __init__(self, *args):
        Comida.__init__(self )
        Vestuario.__init__(self)




class Persona(metaclass = ABCMeta):
    def __init__(self, nombre, fecha_nacimiento):
        self.nombre = nombre
        self._fecha_nacimiento = fecha_nacimiento  ## AAAA-MM-DD

    @property
    def fecha_nacimiento(self):
        año = self._fecha_nacimiento[0:4]
        mes = self._fecha_nacimiento[5:7]
        dia = self._fecha_nacimiento[8:]
        año_actual = time.strftime("%Y", time.gmtime())
        mes_actual = time.strftime("%m", time.gmtime())
        dia_actual = time.strftime("%j", time.gmtime())
        diferencia = int(año_actual) - int(año)
        if dia_actual >= dia:
            return diferencia
        else:
            return (diferencia - 1)



class Cliente(Persona):  # come todo
    def __init__(self, nombre, fecha_nacimiento, monto_dinero):
        super().__init__(nombre, fecha_nacimiento)
        self.monto_dinero = monto_dinero
        self.carro = []
        self.frecuente = False  # parte siendo normal
        self.tercera_edad = False

    def saludo(self):
        return print("Hola.")

    def agregar_producto(self, producto):
        self.carro.append(producto)

    def determinar_tercera_edad(self):
        if self.fecha_nacimiento > 60:
            self.tercera_edad = True
        else:
            self.tercera_edad = False



class Vegano(Cliente):  # verdura
    def __init__(self, nombre, fecha_nacimiento, monto_dinero):
        super().__init__(nombre, fecha_nacimiento, monto_dinero)

    def agregar_producto(self, producto):
        if isinstance(producto, Carne) or isinstance(producto, Lacteo):
            print("No puede entrar al carro, porque no me gusta. ")
        else:
            self.carro.append(producto)

class Vegetariano(Cliente):  # verdura y lacteo
    def __init__(self, nombre, fecha_nacimiento, monto_dinero):
        super().__init__(nombre, fecha_nacimiento, monto_dinero)

    def agregar_producto(self, producto):
        if isinstance(producto, Carne):
            print("No puede entrar al carro, porque no me gusta. ")
        else:
            self.carro.append(producto)



class Cajero(Persona):
    def __init__(self, nombre, fecha_nacimiento):
        super().__init__(nombre, fecha_nacimiento)
        self.caja = []

    def saludo(self):

        return print("Bienvenido estimado.")

    def calcular_compra(self, carro, cliente):
        self.saludo()
        cliente.saludo()
        total_a_pagar = 0
        for objeto in carro:
            if cliente.frecuente:  # Aca aplicamos el descuento correspondiente
                if isinstance(objeto, Vestuario):
                    total_a_pagar += int(objeto.precio) * 0.9
                elif isinstance(objeto, Comida):
                    total_a_pagar += int(objeto.precio) * 0.85

            elif cliente.tercera_edad:
                if isinstance(objeto, Vestuario):
                    total_a_pagar += int(objeto.precio) * 0.9
                elif isinstance(objeto, Comida):
                    total_a_pagar += int(objeto.precio) * 0.9
            else:
                total_a_pagar += int(objeto.precio)
        if total_a_pagar > cliente.monto_dinero:
            return print("No tienes dinero suficiente.")
        else:
            cliente.monto_dinero -= total_a_pagar

        return print("El total a pagar es " + str(total_a_pagar) + ". Que disfrute su dia.")


if __name__ == "__main__":
    cajero1 = Cajero("Daniel", "1994-01-25")
    cliente1 = Cliente("Max", "1996-10-24", 10000)
    cliente2 = Cliente("Lucas Valenzuela", "1950-05-25", 50000)
    cliente2.determinar_tercera_edad()
    vegetariano = Vegetariano("Alex", "1995-06-30", 12000)
    lacteo = Lacteo("yoghurt", "9129394949", "5000", "300", "10", "100", "10", "2019-10-05", "10")
    verdura = Verdura("brocoli", "9129394948", "3000", "300", "10", "100", "10", "2019-10-05", "10")
    carne = Carne("filete", "9129394947", "6000", "300", "100", "10", "10", "2019-10-05", "vacuno")
    prenda1 = Vestuario(46, "hombre", "pantalon", "9129394946", "2000")
    prenda2 = Vestuario(16, "mujer", "polera", "9129394945", "2000")
    prenda3 = Vestuario(35, "niño", "calcetin", "9129394944", "2000")
    comida = Comida("pizza", "9129394943", "5000", "500", "10", "100", "55", "2020-10-25")

    print(cliente2.tercera_edad)
    print(cliente1.fecha_nacimiento)

    #  Compra de prueba cliente 1
    cliente1.agregar_producto(lacteo)
    cajero1.calcular_compra(cliente1.carro, cliente1)
    print(cliente1.monto_dinero)
    cliente1.agregar_producto(carne)
    cajero1.calcular_compra(cliente1.carro, cliente1)


    vegetariano.agregar_producto(carne)

    #pantalon_de_queso = Especial("pantalon de queso", "9129394949", "5000", "300", "10", "100", "10", "2019-10-05",
    #                             "10", 35, "niño")