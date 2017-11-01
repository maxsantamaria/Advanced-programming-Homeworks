import time
import sys
import os
from random import expovariate, randint
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QTransform
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QPushButton)
from threading import Thread
from backend import Character, Enemy


class Movimiento(Thread):
    def __init__(self, trigger_signal, parent):
        super().__init__()
        self.trigger = trigger_signal
        self.parent = parent

    def run(self):
        #i = 2  # sera el numero de la imagen del sprite
        i = 9
        while True:
            if not self.parent.ataque:
                time.sleep(0.1)
                self.trigger.emit("{:0>2d}".format(i))
                i += 1
                if i >= 10:
                    i = 2
            else:
                time.sleep(0.1)
                self.trigger.emit("{:0>2d}".format(i))
                i += 1
                if i >= 12:
                    i = 9


class ApareceEnemigo(Thread):
    def __init__(self, parent, trigger):
        super().__init__()
        self.parent = parent
        self.trigger = trigger

    def run(self):
        while True:
            time.sleep(expovariate(1/10))
            x = randint(0, 900)
            y = randint(0, 500)
            self.trigger.emit(Enemy(self.parent, x, y))


class MiVentana(QWidget):
    threads_response1 = pyqtSignal(object)
    threads_response2 = pyqtSignal(object)
    threads_response3 = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paused = False
        self.ataque = False
        self.enemies = []

        self.init_GUI()
        # Definimos la geometría de la ventana.


    def init_GUI(self):
        # geometria de ventana
        # Parámetros: (x_top_left, y_top_left, width, height)
        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle('DCCell')

        self.label1 = QLabel('Texto:', self)
        self.label1.move(10, 15)

        self.label2 = QLabel('Variable', self)
        self.label2.move(200, 15)

        #self.edit1 = QLineEdit('', self)
        #self.edit1.setGeometry(45, 15, 100, 20)

        self.boton1 = QPushButton('Presiona', self)
        self.boton1.clicked.connect(self.boton_apretado)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.move(5.5, 70)

        # Images Jugador Principal
        self.jug_principal = Character(self, 200, 200)
        self.jug_principal.image = QLabel(self)
        pixmap = QPixmap("Assets/bowser/bowser_02.png")
        pixmap = pixmap.scaled(256 / 2, 256 / 2)
        diag = (pixmap.width()**2 + pixmap.height()**2)**0.5
        self.jug_principal.image.setMinimumSize(diag, diag)
        #self.jug_principal.image.setGeometry(200, 200, 256 * 2, 256 * 2)  # 120, 114
        self.jug_principal.image.setAlignment(Qt.AlignCenter)
        self.jug_principal.image.move(200, 200)
        #pixmap = QPixmap("Assets/main_player/jugador_principal_01.png")

        self.jug_principal.image.setPixmap(QPixmap(pixmap))
        self.jug_principal.image.show()

        # Thread
        #self.label_image.setVisible(True)
        self.threads_response1.connect(self.update_movimiento)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_movimiento2)
        self.numero = 2
        self.timer1.start(100)
        ##self.movimiento = Movimiento(self.threads_response1, self)
        ##self.movimiento.setDaemon(True)
        ##self.movimiento.start()

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.new_enemy2)
        self.timer2.start(expovariate(1 / 10) * 1000)
        self.threads_response2.connect(self.new_enemy)
        ##self.aparicion_enemigos = ApareceEnemigo(self, self.threads_response2)
        ##self.aparicion_enemigos.setDaemon(True)
        ##self.aparicion_enemigos.start()
        self.show()

        self.threads_response3.connect(self.update_position)

        #self.label_image.setPixmap(pixmap)
        #self.label_image.show()

    def update_movimiento2(self):
        pixmap = QPixmap("Assets/bowser/bowser_" + "{:0>2d}".format(self.numero) +
                         ".png")
        pixmap = pixmap.transformed(QTransform().
                                    rotate(self.jug_principal.rotation))
        pixmap = pixmap.scaled(pixmap.width()/4, pixmap.height()/4)
        #pixmap = pixmap.scaled(256/2, 256/2)
        self.jug_principal.image.setPixmap(QPixmap(pixmap))
        for enemigo in self.enemies:
            label = enemigo.image
            pixmap = QPixmap("Assets/clubba/clubba_" + "{:0>2d}".format(self.numero) +
                             ".png")
            pixmap = pixmap.scaled(256 / 4, 256 / 4)
            pixmap = pixmap.transformed(QTransform().
                                        rotate(enemigo.rotation))
            label.setPixmap(QPixmap(pixmap))
        self.numero += 1
        if self.numero >= 10:
            self.numero = 2

    def update_movimiento(self, numero):
        pixmap = QPixmap("Assets/bowser/bowser_" + numero +
                         ".png")
        pixmap = pixmap.transformed(QTransform().
                                    rotate(self.jug_principal.rotation))
        pixmap = pixmap.scaled(pixmap.width()/4, pixmap.height()/4)
        #pixmap = pixmap.scaled(256/2, 256/2)
        self.jug_principal.image.setPixmap(QPixmap(pixmap))
        for enemigo in self.enemies:
            label = enemigo.image
            pixmap = QPixmap("Assets/clubba/clubba_" + numero +
                             ".png")
            pixmap = pixmap.scaled(256 / 4, 256 / 4)
            pixmap = pixmap.transformed(QTransform().
                                        rotate(enemigo.rotation))
            label.setPixmap(QPixmap(pixmap))

    def new_enemy2(self):
        x = randint(0, 900)
        y = randint(0, 500)
        enemy = Enemy(self, x, y)
        label = QLabel(self)
        ##label.setGeometry(enemy.x, enemy.y, 100, 100)  # 120, 114
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("Assets/clubba/clubba_02.png")
        pixmap = pixmap.transformed(QTransform().
                                    rotate(enemy.rotation))
        pixmap = pixmap.scaled(256 / 4, 256 / 4)
        diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        label.setMinimumSize(diag, diag)
        label.setPixmap(QPixmap(pixmap))
        label.move(enemy.x, enemy.y)
        label.show()
        enemy.image = label
        enemy.start()
        self.enemies.append(enemy)

        self.timer2.stop()
        self.timer2.start(expovariate(1 / 10) * 1000)

    def new_enemy(self, enemy):
        label = QLabel(self)
        ##label.setGeometry(enemy.x, enemy.y, 100, 100)  # 120, 114
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("Assets/clubba/clubba_02.png")
        pixmap = pixmap.transformed(QTransform().
                                    rotate(enemy.rotation))
        pixmap = pixmap.scaled(256 / 4, 256 / 4)
        diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        label.setMinimumSize(diag, diag)
        label.setPixmap(QPixmap(pixmap))
        label.move(enemy.x, enemy.y)
        label.show()
        enemy.image = label
        enemy.start()
        self.enemies.append(enemy)

    def boton_apretado(self):
        print('Se apretó')
        sender = self.sender()
        self.label2.setText('Presionando boton {}'.format(sender.text()))
        self.label2.resize(self.label2.sizeHint())

    def keyPressEvent(self, QKeyEvent):
        ctrl = False
        if QKeyEvent.modifiers() == Qt.ControlModifier and \
                QKeyEvent.key() == 83:
            if not self.paused:
                self.timer1.stop()
                self.timer2.stop()
                for enemigo in self.enemies:
                    enemigo.pause()
                self.paused = True
            else:
                self.timer1.start(100)
                self.timer2.start(expovariate(1 / 10) * 1000)  # HAY QUE GUARDAR EL TIEMPO DE ANTES
                for enemigo in self.enemies:
                    enemigo.resume()
                self.paused = False
        print('Presionaron la tecla {}'.format(QKeyEvent.text()))
        if QKeyEvent.text() == "a":
            pixmap = self.jug_principal.image.pixmap().transformed(QTransform()
                                                                   .rotate(-1
                                                                           ))
            self.jug_principal.image.setPixmap(QPixmap(pixmap))
            self.jug_principal.rotation -= 1
        elif QKeyEvent.text() == "d":
            pixmap = self.jug_principal.image.pixmap().transformed(QTransform()
                                                                   .rotate(1))
            self.jug_principal.image.setPixmap(QPixmap(pixmap))
            self.jug_principal.rotation += 1
        elif QKeyEvent.text() == "f":
            self.ataque = True
        elif QKeyEvent.text() == "g":
            self.ataque = False

        self.jug_principal.avanzar2(QKeyEvent)
        self.jug_principal.image.move(self.jug_principal.x,
                                      self.jug_principal.y)

    def update_position(self, enemy):
        enemy.image.move(enemy.x, enemy.y)


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)


    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    window = MiVentana()
    sys.exit(app.exec_())