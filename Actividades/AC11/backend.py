import os.path


class Usuario:

    def __init__(self, nombre, valor_ultima_apuesta, valor_maxima_apuesta, saldo):
        self.nombre = nombre
        self._valor_ultima_apuesta = valor_ultima_apuesta
        self._valor_maxima_apuesta = valor_maxima_apuesta
        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    @property
    def valor_ultima_apuesta(self):
        return self._valor_ultima_apuesta

    @valor_ultima_apuesta.setter
    def valor_ultima_apuesta(self, value):
        self._valor_ultima_apuesta = value


    @property
    def valor_maxima_apuesta(self):
        return self._valor_maxima_apuesta

    @valor_maxima_apuesta.setter
    def valor_maxima_apuesta(self, value):
        self._valor_maxima_apuesta = value


    def datos_para_archivo(self):
        return "{}|{}|{}|{}\n".format(self.nombre, self.valor_ultima_apuesta, self.valor_maxima_apuesta, self.saldo)



    def cambiar_apuesta_maxima(self, apuesta):  # apuesta en str
        apuesta_int = int(apuesta)
        if apuesta_int > self.valor_maxima_apuesta:
            self.valor_maxima_apuesta = apuesta_int


    def __repr__(self):
        return "{}|{}|{}|{}\n".format(self.nombre, self.valor_ultima_apuesta,
                                      self.valor_maxima_apuesta, self.saldo)


def verificar_usuario(nombre):
    existencia = os.path.exists("usuarios.txt")
    if not existencia:
        with open("usuarios.txt", "w") as file:
            usuario = Usuario(nombre, 0, 0, 1500)
            file.write(usuario.datos_para_archivo())

    elif existencia:
        print("a")
        with open("usuarios.txt", "r") as file:
            datos_usuario = list(filter(lambda x: x.strip().split("|")[0] == nombre, [linea for linea in file]))
            print(datos_usuario)
            datos_usuario = datos_usuario[0].strip().split("|")
            print(datos_usuario)
            usuario = Usuario(*datos_usuario)
    return usuario


def guardar_informacion(usuario):
	esplitear = lambda x: x.split("|")
	with open("usuarios.txt", "r") as file:
		usuarios_lista = [esplitear(linea) for linea in file]	
		nuevos_datos_usuario = [usuario.nombre, usuario.valor_ultima_apuesta, usuario.valor_maxima_apuesta, usuario.saldo]
	for i in range(len(usuarios_lista)):
		if usuarios_lista[i][0] == nuevos_datos_usuario[0]:
			indice = i
	usuarios_lista[i] = nuevos_datos_usuario
	with open("usuarios.txt", "w") as file:
		file.write(usuario_x.join("|") for usuario_x in usuarios_lista)





