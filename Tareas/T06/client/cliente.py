from handle_image import Image, leer_estructura_chunk
from PyQt5.QtCore import pyqtSignal, QObject
from eventos import ActualizarImagenEvent, ImagenEditadaEvent, \
    CambioUsuariosEvent, CambiarBotonEditarEvent, ActualizarComentarioEvent
import pickle
import socket
import threading
import time
import os

# HOST = 'localhost'
HOST = '192.168.2.104'
PORT = 1234


class Client(QObject):

    trigger_resultados = pyqtSignal(ActualizarImagenEvent)
    trigger_resultados2 = pyqtSignal(ImagenEditadaEvent)
    trigger_usuarios_conectados = pyqtSignal(CambioUsuariosEvent)
    trigger_advertencia = pyqtSignal(str)
    trigger_boton_editar = pyqtSignal(CambiarBotonEditarEvent)
    trigger_comentario = pyqtSignal(ActualizarComentarioEvent)

    def __init__(self, nombre, window=None, window_registro=None):
        super().__init__()
        print("Inicializando cliente")
        self.nombre = nombre
        self.window = window
        self.window_registro = window_registro
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(socket.gethostbyname(socket.gethostname()))
        self.editor = None

        try:
            self.socket_cliente.connect((HOST, PORT))
            print("Cliente conectado exitosamente al servidor...")

            self.connected = True
            msg = {'status': 'nombre_usuario', 'data': self.nombre}
            self.send(msg)

            thread = threading.Thread(target=self.listen_thread)
            thread.start()
            print("Escuchando al servidor...")

            self.trigger_resultados.connect(window.show_galeria)
            self.trigger_resultados2.connect(window.actualizar_galeria)
            self.trigger_usuarios_conectados.connect(window.usuarios_online)
            self.trigger_advertencia.connect(window.warning)
            self.trigger_boton_editar.connect(window.boton_editar)
            self.trigger_comentario.connect(window.actualizar_comentarios)

        except ConnectionRefusedError:
            # Si la conexión es rechazada, entonces se 'cierra' el socket
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    def entra(self):
        msg = {'status': 'nombre_usuario', 'data': self.nombre}
        self.send(msg)

    def listen_thread(self):
        while self.connected:
            response_bytes_length = self.socket_cliente.recv(4)
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")
            response = bytearray()
            while len(response) < response_length:
                response += self.socket_cliente.recv(256)
            decoded = pickle.loads(response)
            # print(decoded)
            self.handlecommand(decoded)  # era decoded

    def handlecommand(self, decoded):
        if "ingresar_imagen" in decoded["status"]:
            num = decoded["status"][-1]
            event = ActualizarImagenEvent(decoded["nombre"],
                                          bytearray(decoded["data"]), int(num),
                                          decoded["comments"])
            self.trigger_resultados.emit(event)
        elif decoded["status"] == "actualizar_galeria":
            event = ImagenEditadaEvent(decoded["nombre"],
                                       decoded["data"])
            self.trigger_resultados2.emit(event)
        elif decoded["status"] == "editor":
            self.editor = True
        elif decoded["status"] == "espectador":
            self.editor = False
        elif decoded["status"] == "ya_existe":
            self.trigger_advertencia.emit("El nombre de usuario ya existe.")
        elif decoded["status"] == "usuario_entra":
            evento = CambioUsuariosEvent(decoded["data"], True)
            self.trigger_usuarios_conectados.emit(evento)
        elif decoded["status"] == "usuario_sale":
            if decoded["data"] == self.nombre:
                # sys.exit()
                pass
            else:
                evento = CambioUsuariosEvent(decoded["data"], False)
                self.trigger_usuarios_conectados.emit(evento)

        elif decoded["status"] == "alguien_esta_editando":
            evento = CambiarBotonEditarEvent(decoded["nombre"], False)
            self.trigger_boton_editar.emit(evento)
        elif decoded["status"] == "nuevo_comentario":
            evento = ActualizarComentarioEvent(decoded["nombre"],
                                               decoded["data"])
            self.trigger_comentario.emit(evento)

    def enviar_actualizacion(self, event):
        mensaje = {'status': 'actualizar_imagen',
                   'data': event.new_idat_info, 'nombre': event.nombre}
        self.send(mensaje)

    def avisar_edicion(self, nombre):
        mensaje = {'status': 'empieza_edicion', 'nombre': nombre}
        self.send(mensaje)

    def avisar_fin_edicion(self, nombre):
        if self.editor:
            mensaje = {'status': 'fin_edicion', 'nombre': nombre}
            self.send(mensaje)
        self.editor = None

    def avisar_salida(self):
        mensaje = {'status': 'usuario_sale', 'data': self.nombre}
        self.send(mensaje)

    def comentar(self, evento):
        mensaje = {'status': 'nuevo_comentario',
                   'data': [evento.comentario,
                            self.nombre, time.strftime('%c') + "\n"],
                   'nombre': evento.nombre}
        self.send(mensaje)

    def subir_imagen(self, path):
        with open(path, "rb") as file:
            png_bytes = file.read()
            basename = os.path.basename(path)
            nombre = os.path.splitext(basename)[0]
            mensaje = {'status': 'nueva_imagen',
                       'data': png_bytes,
                       'nombre': nombre}
            self.send(mensaje)

    def send(self, msg):
        msg_bytes = pickle.dumps(msg)

        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.send(msg_length + msg_bytes)


if __name__ == "__main__":

    client = Client("Max")
