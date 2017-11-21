import threading
import socket
import pickle
import time
import zlib
import os
import random


# HOST = 'localhost'
HOST = '192.168.2.104'
PORT = 1234


class Server:

    def __init__(self):
        print("Inicializando servidor...")
        if not os.path.exists("image"):
            os.makedirs("image")

        self.socket_servidor = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)

        self.socket_servidor.bind((HOST, PORT))
        print("Dirección y puerto enlazados..")

        self.usuarios = {}  # usuarios en linea
        self.sockets = []
        # despues va a ser con un for de las imagenes en carpeta image
        self.editando_imagenes = {}
        for image in os.listdir("image"):
            nombre = os.path.splitext(image)[0]
            self.editando_imagenes[nombre] = False
        self.socket_servidor.listen(10)
        print("Servidor escuchando en {}:{}...".format(HOST, PORT))

        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()
        print("Servidor aceptando conexiones...")

    def accept_connections_thread(self):

        while True:
            client_socket, _ = self.socket_servidor.accept()

            print("Servidor conectado a un nuevo cliente...")

            self.sockets.append(client_socket)
            # self.enviar_imagenes(client_socket)

            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    def enviar_imagenes(self, client_socket):
        folder = "image"
        i = 0
        imagenes = os.listdir(folder)
        while i < 6 and len(imagenes) > 0:
            image = random.choice(imagenes)
            imagenes.remove(image)
            nombre = os.path.splitext(image)[0]
            with open(os.path.join(folder, image), "rb") as file:
                info = file.read()
                status = 'ingresar_imagen' + str(i)
                mensaje = {'status': status, 'data': info,
                           'nombre': nombre, 'comments': []}
            if not os.path.exists(os.path.join("comments", nombre + ".txt")):
                if not os.path.exists("comments"):
                    os.makedirs("comments")
                with open(os.path.join("comments", nombre + ".txt"), "w") as \
                        file:
                    pass
            else:
                with open(os.path.join("comments", nombre + ".txt"), "r") as \
                        file:
                    comentarios = []
                    for line in file:
                        comentarios.append(line.split(","))
                    mensaje["comments"] = comentarios

            self.send(mensaje, client_socket)
            time.sleep(0.1)
            i += 1

    def listen_client_thread(self, client_socket):
        while True:
            response_bytes_length = client_socket.recv(4)
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")
            response = bytearray()
            while len(response) < response_length:
                response += client_socket.recv(256)
            decoded = pickle.loads(response)
            self.handle_command(decoded, client_socket)
            if decoded["status"] == "usuario_sale":
                print("Usuario se ha desconectado exitosamente")
                client_socket.close()
                break

    def handle_command(self, received, client_socket):
        # print("RECIBI LA IMAGEN ACTUALIZADA")
        if received["status"] == "actualizar_imagen":
            with open("image/" + received["nombre"] + ".png", "rb") as file:
                bytes_png = file.read()
                # esto lo voy a usar para guardarla
                nuevos_bytes_png = cambiar_idat(bytes_png, received["data"])
                mensaje = {'status': 'actualizar_galeria',
                           'data': received['data'],
                           'nombre': received['nombre']}
                for c_socket in self.sockets:
                    self.send(mensaje, c_socket)
            with open(os.path.join("image", received["nombre"] + ".png"),
                      "wb") as file:
                file.write(nuevos_bytes_png)
        elif received["status"] == "nombre_usuario":
            if received["data"] not in self.usuarios.keys():
                self.enviar_imagenes(client_socket)
                time.sleep(0.1)
                mensaje = {'status': 'usuario_entra',
                           'data': received["data"]}
                for c_socket in self.usuarios.values():  # era self.sockets
                    self.send(mensaje, c_socket)
                self.usuarios[received["data"]] = client_socket
                time.sleep(0.1)
                for name in self.usuarios.keys():
                    mensaje['data'] = name
                    self.send(mensaje, client_socket)
            else:
                mensaje = {'status': 'ya_existe'}
                self.send(mensaje, client_socket)

        elif received["status"] == "usuario_sale":
            mensaje = {'status': 'usuario_sale',
                       'data': received["data"]}
            for c_socket in self.usuarios.values():
                self.send(mensaje, c_socket)
            del self.usuarios[received["data"]]
            self.sockets.remove(client_socket)

        elif received["status"] == "empieza_edicion":
            if self.editando_imagenes[received["nombre"]]:
                mensaje = {'status': 'espectador',
                           'nombre': received["nombre"]}
            else:
                mensaje = {'status': 'editor',
                           'nombre': received["nombre"]}
                self.editando_imagenes[received["nombre"]] = True
            self.send(mensaje, client_socket)
        elif received["status"] == "fin_edicion":
            self.editando_imagenes[received["nombre"]] = False
        elif received["status"] == "nuevo_comentario":
            archivo = received["nombre"] + ".txt"
            with open(os.path.join("comments", archivo), "a") as file:
                file.write(",".join(received["data"]))
            mensaje = {'status': 'nuevo_comentario',
                       'data': received["data"],
                       'nombre': received["nombre"]}
            for c_socket in self.usuarios.values():
                self.send(mensaje, c_socket)
        elif received["status"] == "nueva_imagen":
            self.editando_imagenes[received["nombre"]] = False
            archivo = received["nombre"] + ".png"
            with open(os.path.join("image", archivo), "wb") as file:
                file.write(received["data"])

    def send(self, msg, client_socket):
        mensaje_pickle = pickle.dumps(msg)

        msg_length = len(mensaje_pickle).to_bytes(4, byteorder="big")
        client_socket.send(msg_length + mensaje_pickle)


def cambiar_idat(bytes_png, nueva_informacion_idat):
    header = bytes_png[:8]
    body = bytes_png[8:]
    i = 0

    while True:
        largo_informacion = int.from_bytes(body[i:i + 4], byteorder="big")
        tipo_de_bloque = body[i + 4: i + 8].decode()
        if tipo_de_bloque == "IEND":
            iend = body[i: i + 12 + largo_informacion]
            break
        elif tipo_de_bloque == "IHDR":
            ihdr = body[i: i + 12 + largo_informacion]
        i += 12 + largo_informacion
    total = bytearray()
    total += header
    total += ihdr
    largo_informacion_idat = len(nueva_informacion_idat)
    total += largo_informacion_idat.to_bytes(4, byteorder="big")
    tipo = "IDAT".encode()
    total += tipo
    total += nueva_informacion_idat
    idat_crc = zlib.crc32(tipo + nueva_informacion_idat)
    crc = idat_crc.to_bytes(4, byteorder="big")
    total += crc
    total += iend
    return total


if __name__ == "__main__":
    server = Server()

    # Mantenemos al server corriendo
    while True:
        pass
