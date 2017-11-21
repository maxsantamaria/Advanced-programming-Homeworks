from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, \
    QPushButton, QProgressBar, QScrollArea, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from cliente import Client
from handle_image import *
from eventos import ImagenEditadaEvent, ActualizarComentarioEvent
from threading import Thread
import sys
import os


class Inicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle("Ventana de Ingreso")

        # self.cliente = Client()
        self.lab_nombre = QLabel("Ingresa tu nombre sin espacios ni carácteres"
                                 " especiales:\nMínimo 2 caract.", self)

        self.lab_nombre.move(200, 300)
        self.nombre = QLineEdit(self)
        self.nombre.setGeometry(500, 300, 200, 30)
        self.nombre.returnPressed.connect(self.checkear_ingreso)
        self.warning = QLabel()
        self.warning.setGeometry(500, 300, 400, 100)
        self.warning.setStyleSheet("QLabel {color: red}")
        self.warning.setAlignment(Qt.AlignCenter)

        self.show()

    def checkear_ingreso(self):
        if True:
            # self.cliente = Client()
            if len(self.nombre.text()) >= 2 and self.nombre.text().isalnum():
                self.close()
                self.dashboard = Dashboard(self.nombre.text())
            elif len(self.nombre.text()) < 2:
                self.warning.setText("Debe tener al menos 2 caracteres")
                self.warning.show()
            elif not self.nombre.text().isalnum():
                self.warning.setText("Debe ser alphanumerico y sin espacios")
                self.warning.show()


class Dashboard(QWidget):
    trigger_inicio_edicion = pyqtSignal(str)
    trigger_edicion = pyqtSignal(ImagenEditadaEvent)
    trigger_fin_edicion = pyqtSignal(str)
    trigger_nuevo_archivo = pyqtSignal(str)

    def __init__(self, nombre_usuario):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.init_gui()

    def warning(self, advertencia):
        self.warning = QLabel()
        self.warning.setGeometry(500, 300, 400, 100)
        self.warning.setStyleSheet("QLabel {color: red}")
        self.warning.setAlignment(Qt.AlignCenter)
        self.warning.setText(advertencia)
        self.new_name = QLineEdit(self.warning)
        self.new_name.move(100, 70)
        self.new_name.returnPressed.connect(self.nuevo_nombre)
        self.warning.show()

    def nuevo_nombre(self):
        self.cliente.nombre = self.new_name.text()
        self.cliente.entra()
        self.warning.close()

    def init_gui(self):
        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle("Dashboard")
        self.cliente = Client(self.nombre_usuario, self)
        self.labels = []
        self.botones = []
        for i in range(0, 6):
            label = QLabel(self)
            self.boton = QPushButton("Editar", self)
            if i > 2:
                label.move(100 + (i - 3) * 250, 300)
                self.boton.setGeometry(100 + (i - 3) * 250, 510, 200, 40)
            else:
                label.move(100 + (i * 250), 20)
                self.boton.setGeometry(100 + (i * 250), 230, 200, 40)
            self.boton.setVisible(False)
            # self.boton.clicked.connect(lambda : self.abrir_editor(i))
            self.botones.append(self.boton)
            self.labels.append(label)
        self.botones[0].clicked.connect(lambda: self.abrir_editor(0))
        self.botones[1].clicked.connect(lambda: self.abrir_editor(1))
        self.botones[2].clicked.connect(lambda: self.abrir_editor(2))
        self.botones[3].clicked.connect(lambda: self.abrir_editor(3))
        self.botones[4].clicked.connect(lambda: self.abrir_editor(4))
        self.botones[5].clicked.connect(lambda: self.abrir_editor(5))
        self.images = [None, None, None, None, None, None]

        self.boton_subir_archivo = QPushButton("Subir archivo", self)
        self.boton_subir_archivo.move(900, 520)
        self.boton_subir_archivo.clicked.connect(self.subir_archivo)

        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.move(900, 550)
        self.boton_salir.clicked.connect(self.salir)

        self.scroll_usuarios = QScrollArea(self)
        self.scroll_usuarios.setGeometry(900, 50, 100, 100)
        self.show()

        self.usuarios = ["CONECTADOS"]
        self.edicion = None
        self.trigger_inicio_edicion.connect(self.cliente.avisar_edicion)
        self.trigger_edicion.connect(self.cliente.enviar_actualizacion)
        self.trigger_fin_edicion.connect(self.cliente.avisar_fin_edicion)
        self.trigger_nuevo_archivo.connect(self.cliente.subir_imagen)

    def subir_archivo(self):
        self.file = QFileDialog(self)
        self.file.setVisible(True)
        self.file.fileSelected.connect(self.mandar_archivo)

    def mandar_archivo(self):
        print(self.file.selectedFiles()[0])
        print(os.path.basename(self.file.selectedFiles()[0]))
        self.trigger_nuevo_archivo.emit(self.file.selectedFiles()[0])

    def show_galeria(self, event):
        pmap = QPixmap()
        pmap.loadFromData(bytes(event.data), "PNG")
        # label = QLabel(self)
        # label.move(0, 0)
        pmap = pmap.scaled(200, 200)
        label = self.labels[event.num_imagen]
        label.setPixmap(pmap)
        label.resize(200, 200)
        label.show()
        boton = self.botones[event.num_imagen]
        boton.setVisible(True)

        # imagen
        header = event.data[0:8]
        body = event.data[8:]
        new_image = leer_estructura_chunk(body)
        new_image.nombre = event.nombre
        new_image.header = header
        new_image.comentarios = event.comentarios
        new_image.generar_matriz_rgb()
        self.images[event.num_imagen] = new_image

    def actualizar_galeria(self, event):
        print("ACA ACTUALIZO GALERIA")
        for indice, image in enumerate(self.images):
            if image is not None and image.nombre == event.nombre:
                image.idat.informacion = event.new_idat_info
                image.idat.largo_informacion = len(event.new_idat_info)
                image.generar_matriz_rgb()
                pmap = QPixmap()
                pmap.loadFromData(bytes(image.bytes_archivo), "PNG")
                pmap = pmap.scaled(200, 200)
                self.labels[indice].setPixmap(pmap)
        if self.cliente.editor is not None and not self.cliente.editor:
            if self.edicion.isVisible() and \
                    self.edicion.imagen.nombre == event.nombre:
                self.edicion.actualizar_imagen()

    def actualizar_comentarios(self, event):
        for image in self.images:
            if image is not None and image.nombre == event.nombre:
                image.comentarios.append(event.comentario)
                break
        if self.cliente.editor is not None:
            if self.edicion.isVisible() and \
                    self.edicion.imagen.nombre == event.nombre:
                print("ACTUALIZA LO Q QUIERO")
                self.edicion.actualizar_comentario()

    def usuarios_online(self, event):
        if event.entra:
            self.usuarios.append(event.nombre_usuario)
        else:
            self.usuarios.remove(event.nombre_usuario)
        self.label_usuarios = QLabel(self)
        self.label_usuarios.setText("\n".join(self.usuarios))
        self.scroll_usuarios.setWidget(self.label_usuarios)

    def boton_editar(self, event):
        # se puede usar para mostrar que alguien esta editando
        for imagen in self.images:
            if imagen.nombre == event.nombre:
                indice = self.images.index(imagen)
                boton = self.botones[indice]
                if not event.editable:
                    boton.setText("Alguien está editando...")
                else:
                    boton.setText("Editar")
                break

    def abrir_editor(self, numero_imagen):
        self.trigger_inicio_edicion.emit(self.images[numero_imagen].nombre)
        while self.cliente.editor is None:
            pass
        self.edicion = Editor(self, numero_imagen, self.cliente.editor)

    def cursor(self):
        self.boton_recortar.setEnabled(True)
        self.boton_cursor.setEnabled(False)

    def recortar(self):
        self.boton_recortar.setEnabled(False)
        self.boton_cursor.setEnabled(True)

    def salir(self):

        self.cliente.connected = False
        self.cliente.avisar_salida()
        # self.cliente.socket_cliente.close()

        self.close()
        self.nuevo_inicio = Inicio()
        # sys.exit()

    def closeEvent(self, QCloseEvent):  # no vuelve al inicio
        self.cliente.connected = False
        self.cliente.avisar_salida()
        self.close()


class Editor(QWidget):
    trigger_comentario = pyqtSignal(ActualizarComentarioEvent)

    def __init__(self, parent, numero_imagen, editor):
        super().__init__()
        self.parent = parent
        self.numero_imagen = numero_imagen
        self.imagen = parent.images[numero_imagen]
        pmap = QPixmap()
        pmap.loadFromData(bytes(self.imagen.bytes_archivo))
        self.setGeometry(200, 20, pmap.width() + 200, pmap.height())
        self.label = QLabel(self)
        self.label.setPixmap(pmap)
        self.label.move(0, 0)

        self.label_comentarios = QLabel(self)
        mostrar = "<html>"
        for comentario in self.imagen.comentarios:
            #mostrar += comentario[0] + " por " + comentario[1] + " | " + \
            #          comentario[2]
            form = format_comentarios(comentario)
            mostrar += form
            #mostrar += comentario[0] + " <b>por " + comentario[1] +\
            #           "</b> | " + comentario[2] + "<img src=emojis/emot_09.png style=width:5px;height:5px;> " + "<br/>"
        mostrar += "</html>"
        self.label_comentarios.setText(mostrar)
        self.scroll_comentarios = QScrollArea(self)
        self.scroll_comentarios.setGeometry(pmap.width(), 340, 190, 150)
        self.scroll_comentarios.setWidget(self.label_comentarios)
        self.escribir_comentario = QLineEdit(self)
        self.escribir_comentario.setGeometry(pmap.width(), 490, 190, 20)
        self.escribir_comentario.returnPressed.connect(self.comentar)
        self.comm = QLabel("COMENTARIOS", self)
        self.comm.setStyleSheet("QLabel {font-weight: bold; font-size: 10px;"
                                "font-family: Courier}")
        self.comm.move(pmap.width(), 325)


        # botones
        self.boton_cursor = QPushButton("Cursor", self)
        self.boton_cursor.move(pmap.width(), 10)
        self.boton_cursor.clicked.connect(self.cursor)

        self.boton_recortar = QPushButton("Recortar", self)
        self.boton_recortar.move(pmap.width(), 30)
        self.boton_recortar.clicked.connect(self.recortar)
        if not editor:
            self.boton_recortar.setEnabled(False)

        self.boton_balde = QPushButton("Balde", self)
        self.boton_balde.move(pmap.width(), 50)
        self.boton_balde.clicked.connect(self.balde)
        if not editor:
            self.boton_balde.setEnabled(False)

        self.boton_blurry = QPushButton("Blurry", self)
        self.boton_blurry.move(pmap.width(), 70)
        self.boton_blurry.clicked.connect(self.blurry)
        if not editor:
            self.boton_blurry.setEnabled(False)

        self.boton_descarga = QPushButton("Descargar", self)
        self.boton_descarga.move(pmap.width(), 90)
        self.boton_descarga.clicked.connect(self.descargar)

        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.move(pmap.width(), 300)
        self.boton_salir.clicked.connect(self.salir)

        self.show()
        self.herramienta_recorte = False
        self.herramienta_balde = False
        self.herramienta_blurry = False
        self.pos_inicial = None

        self.trigger_comentario.connect(self.parent.cliente.comentar)

    def descargar(self):
        nombre_archivo = self.imagen.nombre + ".png"
        if not os.path.exists(nombre_archivo):
            with open(nombre_archivo, "wb") as file:
                file.write(self.imagen.bytes_archivo)
        else:
            i = 1
            nombre_archivo = self.imagen.nombre + "({0})" + "{1}"
            while os.path.exists(nombre_archivo.format(i, ".png")):
                i += 1
            with open(nombre_archivo.format(i, ".png"), "wb") as file:
                file.write(self.imagen.bytes_archivo)

    def comentar(self):
        comentario = self.escribir_comentario.text()
        self.escribir_comentario.setText("")
        evento = ActualizarComentarioEvent(self.imagen.nombre,
                                           comentario)
        self.trigger_comentario.emit(evento)

    def cursor(self):
        self.boton_recortar.setEnabled(True)
        self.boton_cursor.setEnabled(False)
        self.boton_balde.setEnabled(True)
        self.boton_blurry.setEnabled(True)
        self.herramienta_recorte = False
        self.herramienta_balde = False
        self.herramienta_blurry = False

    def recortar(self):
        self.boton_recortar.setEnabled(False)
        self.boton_cursor.setEnabled(True)
        self.boton_balde.setEnabled(True)
        self.boton_blurry.setEnabled(True)
        self.herramienta_recorte = True
        self.herramienta_balde = False
        self.herramienta_blurry = False

    def balde(self):
        self.boton_recortar.setEnabled(True)
        self.boton_cursor.setEnabled(True)
        self.boton_balde.setEnabled(False)
        self.boton_blurry.setEnabled(True)
        self.herramienta_recorte = False
        self.herramienta_balde = True
        self.herramienta_blurry = False
        self.colores = QColorDialog(self)
        self.colores.setVisible(True)
        self.colores.colorSelected.connect(self.eligio_color)

    def blurry(self):
        self.boton_recortar.setEnabled(True)
        self.boton_cursor.setEnabled(True)
        self.boton_balde.setEnabled(True)
        self.boton_blurry.setEnabled(False)
        self.herramienta_recorte = False
        self.herramienta_balde = False
        self.herramienta_blurry = True

    def actualizar_imagen(self):
        print("ACTUALIZANDOOOOOOOOOOOOOOO")
        self.imagen = self.parent.images[self.numero_imagen]
        pmap = QPixmap()
        pmap.loadFromData(bytes(self.imagen.bytes_archivo), "PNG")
        self.label.setPixmap(pmap)

    def actualizar_comentario(self):
        self.imagen = self.parent.images[self.numero_imagen]
        mostrar = "<html>"
        for comentario in self.imagen.comentarios:
            form = format_comentarios(comentario)
            mostrar += form
        mostrar += "</html>"
        self.label_comentarios = QLabel(self)
        self.label_comentarios.setText(mostrar)
        self.scroll_comentarios.setWidget(self.label_comentarios)

    def salir(self):
        self.parent.trigger_fin_edicion.emit(self.imagen.nombre)
        self.close()

    def mouseMoveEvent(self, QMouseEvent):
        if self.herramienta_recorte:
            if self.pos_inicial is None:
                self.pos_inicial = QMouseEvent.pos()
                self.recuadro = QLabel(self)
                self.recuadro.setStyleSheet("QLabel {border-width: 2px;"
                                            "border-color: black;"
                                            "border-style: dot-dash}")
                self.recuadro.move(self.pos_inicial)
            if QMouseEvent.y() < self.pos_inicial.y():
                self.recuadro.move(self.recuadro.x(),
                                   QMouseEvent.y())
            if QMouseEvent.x() < self.pos_inicial.x():
                self.recuadro.move(QMouseEvent.x(),
                                   self.recuadro.y())

            self.recuadro.resize(abs(QMouseEvent.x() - self.pos_inicial.x()),
                                 abs(QMouseEvent.y() - self.pos_inicial.y()))
            self.recuadro.show()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.herramienta_recorte:
            if self.pos_inicial is not None:
                self.pos_inicial = None
                v1 = [self.recuadro.x(), self.recuadro.y()]
                v2 = [self.recuadro.x() + self.recuadro.width() - 1,
                      self.recuadro.y() + self.recuadro.height() - 1]
                if v2[0] >= self.label.width():
                    v2[0] = self.label.width() - 1
                if v2[1] >= self.label.height():
                    v2[1] = self.label.height() - 1
                if v1[0] <= self.label.width() and \
                        v2[1] <= self.label.height():
                    self.imagen = recortar_imagen(self.imagen, v1, v2)
                    self.actualizar_label()
                self.recuadro.deleteLater()

    def mousePressEvent(self, QMouseEvent):
        if self.herramienta_balde:
            posicion = [QMouseEvent.x(), QMouseEvent.y()]
            if posicion[0] < self.label.width() and \
                    posicion[1] < self.label.height():
                # self.imagen = balde_azul(self.imagen, posicion)
                # self.actualizar_label()
                self.aviso = QLabel("Se está realizando operacion\n"
                                    "de balde, no hacer nada más...", self)
                self.aviso.move(self.label.width(), 260)
                self.aviso.show()
                self.thread_balde = Thread(target=balde_azul,
                                           args=(self.imagen, posicion,
                                                 self.color_balde,
                                                 self))
                self.thread_balde.start()

        elif self.herramienta_blurry:
            self.pbar = QProgressBar(self)
            self.pbar.setGeometry(100, 200, 300, 20)
            self.pbar.show()
            self.thread_blurry = Thread(target=blurry, args=(self.imagen,
                                                             self))
            # self.imagen = blurry(self.imagen, self.pbar)
            self.thread_blurry.start()

    def actualizar_label(self):
        pmap = QPixmap()
        pmap.loadFromData(bytes(self.imagen.bytes_archivo))
        self.label.setPixmap(pmap)
        self.parent.trigger_edicion.emit(ImagenEditadaEvent
                                         (self.imagen.nombre,
                                          self.imagen.idat.
                                          informacion))

    def eligio_color(self):
        color_byte = bytearray()
        color_byte += self.colores.selectedColor().red().\
            to_bytes(1, byteorder="big")
        color_byte += self.colores.selectedColor().green().\
            to_bytes(1, byteorder="big")
        color_byte += self.colores.selectedColor().blue().\
            to_bytes(1, byteorder="big")
        self.color_balde = color_byte

    def closeEvent(self, QCloseEvent):
        self.salir()


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)


    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    menu = Inicio()
    sys.exit(app.exec_())
