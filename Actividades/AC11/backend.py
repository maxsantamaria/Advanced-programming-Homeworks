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


def verificar_usuario(nombre):
	existencia = os.path.exists("usuarios.txt")
	if not existencia:
		with open("usuarios.txt", "w") as file:
			usuario = Usuario(nombre, 0, 0, 1500)
			file.write(usuario.datos_para_archivo())

	elif existencia:
		with open("usuarios.txt", "r") as file:
			datos_usuario = list(filter(lambda x: x.split("|")[0] == nombre, [linea for linea in file]))

