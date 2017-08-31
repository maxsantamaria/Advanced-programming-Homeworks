class Nodo:
    def __init__(self, letra):
        self.letra = letra
        self.hijos = {}  # key = letra, value = Nodo
        self.numero = 0
        self.id = 0

class ContactTrie:
    def __init__(self, nodo_raiz):
        self.nodo_raiz = nodo_raiz  # instancia Nodo
        #self.hijos = {}


    def agregar_nodo(self, letra, nodo_anterior):
        agregado = False
        temporal = nodo_anterior
        while not agregado:
            if letra in temporal.hijos.keys():
                agregado = True
                return temporal.hijos[letra]
            else:
                nuevo_Nodo = Nodo(letra)
                temporal.hijos.update({letra : nuevo_Nodo})
                agregado = True
                return nuevo_Nodo

    def obtener_cadenas(self):

        def obtener_lista_contactos(nodo_padre):
            for nodo_inicial in nodo_padre.hijos.values():
                self.contacto += nodo_inicial.letra
                if len(nodo_inicial.hijos.items()) > 1:
                    self.aux = self.contacto
                obtener_lista_contactos(nodo_inicial)
                if self.aux != "":
                    self.contacto = self.aux
                    self.partir_de_cero = False
                else:
                    self.partir_de_cero = True

            if nodo_padre.numero != 0 and self.contacto != "":
                self.lista_contactos.append(self.contacto)
                self.contacto = ""

                return
            return
        self.partir_de_cero = False
        self.lista_contactos = []
        self.contacto = ""
        self.aux = ""
        obtener_lista_contactos(self.nodo_raiz)
        return self.lista_contactos

    def add_contact(self, nombre, numero):  # string, int
        if not nombre.isalpha():
            print("Nombre invalido")
            return
        nombre = nombre.upper()
        try:
            if int(numero) <= 0:
                print("Numero invalido")
                return
        except:
            print("Numero invalido")
            return

        if nombre in self.obtener_cadenas():
            print("El nombre ya existe")
            return

        nodo_anterior = self.agregar_nodo(nombre[0], self.nodo_raiz)
        nombre = nombre[1:]
        for letra in nombre:
            nodo_anterior = self.agregar_nodo(letra, nodo_anterior)
            if letra == nombre[-1]:
                nodo_anterior.numero = numero
        print("Contacto agregado con exito.")

    def change_contact_number(self, nombre, nuevo_numero):
        if not nombre.isalpha():
            print("Argumentos invalidos")
            return
        nombre = nombre.upper()
        try:
            if int(nuevo_numero) <= 0:
                print("Argumentos invalidos")
                return
        except:
            print("Argumentos invalidos")
            return
        if nombre not in self.obtener_cadenas():
            print("Contacto inexistente")
            return
        def recorrer2(nodo_padre, contacto_buscado):
            for nodo_inicial in nodo_padre.hijos.values():
                self.contacto += nodo_inicial.letra
                if len(nodo_inicial.hijos.items()) > 1:
                    self.aux = self.contacto
                recorrer2(nodo_inicial, contacto_buscado)
                if self.aux != "":
                    self.contacto = self.aux

            if nodo_padre.numero != 0 and self.contacto != "":
                if self.contacto == contacto_buscado:
                    nodo_padre.numero = nuevo_numero
                self.contacto = ""
                return
            return
        self.contacto = ""
        self.numero = 0
        recorrer2(self.nodo_raiz, nombre)


    def ask_for_contact(self, nombre):
        if not nombre.isalpha():
            print("Nombre invalido")
            return
        nombre = nombre.upper()
        lista_contactos = self.obtener_cadenas()
        if nombre not in lista_contactos:
            print("Nombre no existe")

        def recorrer(nodo_padre, contacto_buscado):
            for nodo_inicial in nodo_padre.hijos.values():
                self.contacto += nodo_inicial.letra
                if len(nodo_inicial.hijos.items()) > 1:
                    self.aux = self.contacto
                recorrer(nodo_inicial, contacto_buscado)
                if self.aux != "":
                    self.contacto = self.aux

            if nodo_padre.numero != 0 and self.contacto != "":
                if self.contacto == contacto_buscado:
                    self.numero = nodo_padre.numero
                self.contacto = ""
                return
            return
        self.numero = 0
        self.contacto = ""
        recorrer(self.nodo_raiz, nombre)
        if int(self.numero) > 0:
            tupla = ({nombre}, {self.numero})
            print(tupla)

    def get_all_contacts(self):
        lista_contactos = self.obtener_cadenas()
        for contacto in lista_contactos:
            self.contacto = ""
            self.numero = 0
            self.ask_for_contact(contacto)

    def merge_tries(self, otro_trie):
        if not isinstance(otro_trie, ContactTrie):
            print("Debe ser un contactrie")
            return
        contactos = otro_trie.obtener_cadenas()
        nueva_lista = set()
        contactos_actuales = self.obtener_cadenas()
        for nuevo_contacto in contactos:
            if nuevo_contacto not in contactos_actuales:
                nuevo_numero = otro_trie.ask_for_contact(nuevo_contacto)
                nodo_anterior = self.nodo_raiz
                for letra in nuevo_contacto:
                    nodo_anterior = self.agregar_nodo(letra, nodo_anterior)
                    if letra == nuevo_contacto[-1]:
                        nodo_anterior.numero = nuevo_numero


    def __repr__(self):

        def recorrer_arbol(raiz):
            for hijo in raiz.hijos.values():
                self.ret += "id-nodo: {} -> id_padre: {} \n".format(
                    hijo.letra, raiz.letra)
                recorrer_arbol(hijo)

            return self

        self.ret = 'RAIZ: -> valor: {}\n\nHIJOS:\n'.format(self.nodo_raiz.letra)
        recorrer_arbol(self.nodo_raiz)
        return self.ret

raiz = Nodo("")
sistema = ContactTrie(raiz)
#nodo1 = sistema.agregar_nodo("h", raiz)
#nodo2 = sistema.agregar_nodo("o", nodo1)
#nodo3 = sistema.agregar_nodo("l", nodo2)
#nodo4 = sistema.agregar_nodo("a", nodo3)
#nodo4.numero = 123

lista = sistema.obtener_cadenas()
print(lista)

#nodo5 = sistema.agregar_nodo("h", raiz)
#nodo6 = sistema.agregar_nodo("a", nodo5)
#nodo6.numero = 321

#print(sistema)

sistema.add_contact("max", 123)
sistema.add_contact("cata", 124)
sistema.add_contact("alejandro", 125)
print(sistema)

# imprime todos los contactos
lista = sistema.obtener_cadenas()
print(lista)


# empiezan las pruebas del sistema
sistema.ask_for_contact("max")
sistema.ask_for_contact("asdasdas")
sistema.get_all_contacts()
sistema.change_contact_number("max", 666)
sistema.ask_for_contact("max")   # vemos que cambio el numero



raiz2 = Nodo("")
sistema2 = ContactTrie(raiz2)

sistema2.add_contact("jorge", "321")
sistema2.add_contact("carla", "456")
sistema2.add_contact("roberto", "567")
sistema2.get_all_contacts()



sistema.merge_tries(sistema2)
sistema.get_all_contacts()