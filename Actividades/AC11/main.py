import sys
import backend
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


formulario = uic.loadUiType("interfaz.ui")
#print(formulario[0], formulario[1])
ingreso = uic.loadUiType("ingresar.ui")


class Casino(formulario[0], formulario[1]):
    def __init__(self, nombre):
        super().__init__()
        self.setupUi(self)
        #self.BotonAumentar.clicke
        self.nombre = nombre
        self.usuario = backend.verificar_usuario(nombre)
        self.saludo.setText("Hola " + self.usuario.nombre)
        self.apuesta_actual.setText(str(self.usuario.saldo))
        self.maximo_premio







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