class Nodo:
    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor


class ListaLigada:
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for elem in args:
            if not self.cabeza:
                self.cabeza = Nodo(elem)
                self.cola = self.cabeza
            else:
                nuevo_nodo = Nodo(elem)
                self.cola.siguiente = nuevo_nodo
                self.cola = nuevo_nodo


    def append(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def remove(self, value):
        nodo_actual = self.cabeza
        while nodo_actual:
            if nodo_actual.valor == value:
                break
            else:
                nodo_actual = nodo_actual.siguiente
        nodo_anterior = self.cabeza
        while nodo_anterior.siguiente != nodo_actual and nodo_actual != self.cabeza:
            nodo_anterior = nodo_anterior.siguiente
        if self.cabeza == nodo_actual:
            self.cabeza = nodo_actual.siguiente
        elif self.cola == nodo_actual:
                nodo_anterior.siguiente = None
                self.cola = nodo_anterior
        else:
            nodo_anterior.siguiente = nodo_actual.siguiente
        del nodo_actual

    def pop(self, key):
        if key < 0:
            key = len(self) + key
        nodo = self.cabeza
        for i in range(key):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            return "posicion no encontrada"
        nodo_anterior = self.cabeza
        for i in range(key - 1):
            if nodo_anterior:
                nodo_anterior = nodo_anterior.siguiente
        if self.cabeza == nodo:
            self.cabeza = nodo.siguiente
        elif self.cola == nodo:
            nodo_anterior.siguiente = None
            self.cola = nodo_anterior
        else:
            nodo_anterior.siguiente = nodo.siguiente
        value = nodo.valor
        del nodo
        return value

    def __getitem__(self, posicion):
        if posicion < 0:
            posicion = len(self) + posicion
        nodo = self.cabeza

        for i in range(posicion):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            return "posicion no encontrada"
        else:
            return nodo.valor

    def __delitem__(self, key):
        if key < 0:
            key = len(self) + key
        nodo = self.cabeza
        for i in range(key):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            return "posicion no encontrada"
        nodo_anterior = self.cabeza
        for i in range(key - 1):
            if nodo_anterior:
                nodo_anterior = nodo_anterior.siguiente
        if self.cabeza == nodo:
            self.cabeza = nodo.siguiente
        elif self.cola == nodo:
                nodo_anterior.siguiente = None
                self.cola = nodo_anterior
        else:
            nodo_anterior.siguiente = nodo.siguiente
        del nodo

    def __setitem__(self, key, value):  # key es el indice
        if key < 0:
            key = len(self) + key
        nodo = self.cabeza
        for i in range(key):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            return "posicion no encontrada"
        else:
            nodo.valor = value

    def __len__(self):
        contador = 0
        nodo_actual = self.cabeza
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            contador += 1
        return contador

    def __iter__(self):
        self.pointer = 0  # para partir en __next__ del comienzo
        #nodo_actual = self.cabeza
        #if nodo_actual:
            #yield nodo_actual.valor

        #while nodo_actual:
            #nodo_actual = nodo_actual.siguiente
            #if nodo_actual:
                #yield nodo_actual.valor
        return self

    def __next__(self):
        if self.pointer == 0:
            self.pointer = self.cabeza
        else:
            self.pointer = self.pointer.siguiente
        if not self.pointer:
            raise StopIteration  # deja de iterar
        else:
            return self.pointer.valor

    def __repr__(self):
        rep = '['
        nodo_actual = self.cabeza

        while nodo_actual:
            rep += '{}'.format(nodo_actual.valor)
            if nodo_actual != self.cola:
                rep += ", "
            nodo_actual = nodo_actual.siguiente
        rep += "]"
        return rep


class Elem:
    def __init__(self, key=None, valor=None):
        self.siguiente = None
        self.key = key
        self.valor = valor


class Diccionario_Ligado:
    def __init__(self):
        self.cola = None
        self.cabeza = None

    def update(self, key, valor):
        if not self.cabeza:
            self.cabeza = Elem(key, valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Elem(key, valor)
            self.cola = self.cola.siguiente

    def __getitem__(self, key):
        nodo = self.cabeza
        while nodo.key != key:
            nodo = nodo.siguiente
            if not nodo:
                break
        if not nodo:
            raise KeyError
            return "posicion no encontrada"
        else:
            return nodo.valor

    def __setitem__(self, key, value):
        nodo = self.cabeza

        while nodo.key != key:
            nodo = nodo.siguiente
            if not nodo:
                break
        if not nodo:
            raise KeyError
            return "posicion no encontrada"
        else:
            nodo.valor = value

    def __delitem__(self, key):
        nodo = self.cabeza
        while nodo.key != key:
            nodo = nodo.siguiente
            if not nodo:
                break
        if not nodo:
            raise EnvironmentError
            return "posicion no encontrada"
        nodo_anterior = self.cabeza  # nodo anterior al que vamos a eliminar
        while nodo_anterior.siguiente != nodo and nodo != self.cabeza:
            nodo_anterior = nodo_anterior.siguiente
        if nodo == self.cabeza:
            self.cabeza = nodo.siguiente
        elif nodo == self.cola:
            self.cola = nodo_anterior
            nodo_anterior.siguiente = None
        else:
            nodo_anterior.siguiente = nodo.siguiente
        del nodo

    def __len__(self):
        contador = 0
        nodo_actual = self.cabeza
        while nodo_actual:
            contador += 1
            nodo_actual = nodo_actual.siguiente
        return contador

    def __iter__(self):
        #nodo_actual = self.cabeza
        #if nodo_actual:
            #yield nodo_actual.key
        #while nodo_actual:
            #nodo_actual = nodo_actual.siguiente
            #if nodo_actual:
                #yield nodo_actual.key
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer == 0:
            self.pointer = self.cabeza
        else:
            self.pointer = self.pointer.siguiente
        if not self.pointer:
            raise StopIteration  # deja de iterar
        else:
            return self.pointer.key


    def values(self):
        nodo_actual = self.cabeza
        iterable = ListaLigada()
        if nodo_actual:
            #yield nodo_actual.valor
            iterable.append(nodo_actual.valor)
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            if nodo_actual:
                iterable.append(nodo_actual.valor)
                #yield nodo_actual.valor
        return iterable

    def keys(self):
        nodo_actual = self.cabeza
        iterable = ListaLigada()
        if nodo_actual:
            iterable.append(nodo_actual.key)
            #yield nodo_actual.key
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            if nodo_actual:
                iterable.append(nodo_actual.key)
                #yield nodo_actual.key
        return iterable

    def items(self):
        nodo_actual = self.cabeza
        iterable = ListaLigada()
        if nodo_actual:
            iterable.append(Tupla(nodo_actual.key, nodo_actual.valor))
            # yield nodo_actual.key
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            if nodo_actual:
                iterable.append(Tupla(nodo_actual.key, nodo_actual.valor))
                # yield nodo_actual.key
        return iterable
        pass

    def __repr__(self):
        rep = '{'
        nodo_actual = self.cabeza
        while nodo_actual:
            rep += '{}:{}'.format(nodo_actual.key, nodo_actual.valor)
            if nodo_actual != self.cola:
                rep += ", "
            nodo_actual = nodo_actual.siguiente
        rep += "}"
        return rep


class Tupla:
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for valor in args:
            new_elem = Nodo(valor)
            if not self.cabeza:
                self.cabeza = new_elem
                self.cola = self.cabeza
            else:
                self.cola.siguiente = new_elem
                self.cola = new_elem

    def __getitem__(self, posicion):
        nodo = self.cabeza
        for i in range(posicion):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            return "posicion no encontrada"
        else:
            return nodo.valor

    def __add__(self, other_tupla):  # este metodo actualiza la tupla actual
        if self.cola:
            self.cola.siguiente = other_tupla.cabeza
        self.cola = other_tupla.cola
        return self

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer == 0:
            self.pointer = self.cabeza
        else:
            self.pointer = self.pointer.siguiente
        if not self.pointer:
            raise StopIteration  # deja de iterar
        else:
            return self.pointer.valor

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(0, len(self)):
            if self[i] != other[i]:
                return False
        return True

    def __len__(self):
        contador = 0
        nodo_actual = self.cabeza
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            contador += 1
        return contador


    def __repr__(self):
        rep = '('
        nodo_actual = self.cabeza
        while nodo_actual:
            rep += '{}'.format(nodo_actual.valor)
            if nodo_actual != self.cola:
                rep += ", "
            nodo_actual = nodo_actual.siguiente
        rep += ")"
        return rep

class MySet:
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for elem in args:
            self.add(elem)

    def add(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            existe = False
            for elem in self:
                if elem == valor:
                    existe = True
                    break
            if not existe:
                self.cola.siguiente = Nodo(valor)
                self.cola = self.cola.siguiente

    def remove(self, value):
        nodo_actual = self.cabeza
        while nodo_actual:
            if nodo_actual.valor == value:
                break
            else:
                nodo_actual = nodo_actual.siguiente
        nodo_anterior = self.cabeza
        while nodo_anterior.siguiente != nodo_actual and nodo_actual != self.cabeza:
            nodo_anterior = nodo_anterior.siguiente
        if self.cabeza == nodo_actual:
            self.cabeza = nodo_actual.siguiente
        elif self.cola == nodo_actual:
                nodo_anterior.siguiente = None
                self.cola = nodo_anterior
        else:
            nodo_anterior.siguiente = nodo_actual.siguiente
        del nodo_actual

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer == 0:
            self.pointer = self.cabeza
        else:
            self.pointer = self.pointer.siguiente
        if not self.pointer:
            raise StopIteration  # deja de iterar
        else:
            return self.pointer.valor

    def __repr__(self):
        rep = '{'
        nodo_actual = self.cabeza
        while nodo_actual:
            rep += '{}'.format(nodo_actual.valor)
            if nodo_actual != self.cola:
                rep += ", "
            nodo_actual = nodo_actual.siguiente
        rep += "}"
        return rep


if __name__ == "__main__":
    print("LISTA")
    lista = ListaLigada()
    lista.append(5)
    lista.append(6)
    lista.append(7)
    print(lista)
    print(lista[-1], "asdasdas")
    print(lista[1], "\n")
    print(len(lista), "\n")
    lista[1] = 10
    for elem in lista:
        print(elem)

    del lista[2]
    print(lista)

    a = lista.pop(0)
    print(lista, a)

    lista2 = ListaLigada(100, 200, 300)
    print(lista2)

    print("DICCIONARIO")
    diccionario = Diccionario_Ligado()
    diccionario.update("hola", 5)
    diccionario.update("chao", 10)
    diccionario.update("volvi", 250)
    print(diccionario["chao"])
    print(diccionario)


    diccionario["hola"] = 0
    print(diccionario)

    del diccionario["chao"]
    print(diccionario)
    print(len(diccionario))

    for elem in diccionario:
        print(elem)

    print(250 in diccionario.values())

    print(diccionario.values())

    print(diccionario.keys())
    print("TUPLA")
    tupla = Tupla(1, 2, 3, 5)
    tupla = tupla + Tupla(6, 7)
    print(tupla)

    sett = MySet()
    sett.add(1)
    sett.add(2)
    sett.add(1)
    print(sett)
    sett = MySet(1, 2, 3, 4, 3, 2, 1)
    print(sett)

    lista_mala = ListaLigada()
    lista_mala.append(1)
    for elem in lista_mala:
        print(elem)