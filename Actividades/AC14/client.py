import threading
import socket
import sys
import json
import time


class Client:
    def __init__(self):
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 1234

        try:
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor...")

            self.connected = True

            thread = threading.Thread(target=self.listen_thread)
            thread.start()
            print("Escuchando al servidor...")

        except ConnectionRefusedError:
            # Si la conexión es rechazada, entonces se 'cierra' el socket
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    def listen_thread(self):
        while self.connected:
            # Primero recibimos los 4 bytes del largo
            response_bytes_length = self.socket_cliente.recv(4)
            # Los decodificamos
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")

            # Luego, creamos un bytearray vacío para juntar el mensaje
            response = bytearray()

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(response) < response_length:
                response += self.socket_cliente.recv(256)

            response = response.decode()

            decoded = json.loads(response)  # diccionario
            self.handlecommand(decoded)

    def handlecommand(self, decoded):
        #print("Mensaje Recibido: {}".format(decoded))
        tableros = decoded["data"]
        print(tableros)
        if decoded["status"] == "te_toca":
            posicion = input("Ingresa la posición a atacar o "
                             "exit para salir: ")
            if posicion != "exit":
                msg = {"status": "ataque", "data": posicion}
            else:
                msg = {"status": "exit"}
            self.send(msg)
        elif decoded["status"] == "no_te_toca":
            print("Espera...")

        elif decoded["status"] == "termino" or decoded["status"] == "exit":
            print("Conexión terminada")
            self.socket_cliente.close()
            sys.exit()

    def send(self, msg):
        #print("send")
        msg_json = json.dumps(msg)
        msg_bytes = msg_json.encode()

        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        self.socket_cliente.send(msg_length + msg_bytes)


if __name__ == "__main__":
    client = Client()

