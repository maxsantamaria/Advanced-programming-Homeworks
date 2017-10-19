import sys
from backend import verificar_usuario
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


formulario = uic.loadUiType("interfaz.ui")
#print(formulario[0], formulario[1])
ingreso = uic.loadUiType("ingresar.ui")


class Casino(formulario[0], formulario[1]):
    def __init__(self, nombre):
        super().__init__()
        self.setupUi(self)
        self.nombre = nombre
        #self.usuario = verificar_usuario(nombre)
        self.saludo.setText("Hola " + self.nombre)
        #self.apuesta_actual.setText(str(self.usuario.saldo))
        #self.maximo_premio.setText(str(self.usuario.valor_maxima_apuesta))
        #self.ultima_apuesta.setText(str(self.usuario._valor_ultima_apuesta))
        #self.apuesta = 500
        self.saldo_actual.setText(str(1500))
        self.maximo_premio.setText(str(0))
        self.ultima_apuesta.setText(str(0))

        self.apuesta_actual.setText("500")
        self.up.clicked.connect(self.aumentar)
        #self.down.clicked.connect(self.disminuir)

    def aumentar(self):
        self.apuesta += 1
        self.apuesta_actual.setText(str(self.apuesta))


class Register(ingreso[0], ingreso[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ingresar)

    def ingresar(self):
        self.username = self.nombre.text()
        self.casino = Casino(self.username)
        self.casino.show()
        self.close()

class MainWindow:
    def run(self):
        reg = Register()
        reg.show()
        reg.close()


if __name__ == '__main__':
    app = QApplication([])
    reg = Register()
    reg.show()
    #reg.close()

    sys.exit(app.exec_())