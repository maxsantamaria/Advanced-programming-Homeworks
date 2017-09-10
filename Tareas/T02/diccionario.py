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
            raise EnvironmentError
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
            raise EnvironmentError
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
        self.pointer == 0
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
        if nodo_actual:
            yield nodo_actual.valor
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            if nodo_actual:
                yield nodo_actual.valor

    def keys(self):
        nodo_actual = self.cabeza
        if nodo_actual:
            yield nodo_actual.key
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente
            if nodo_actual:
                yield nodo_actual.key

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

