import socket
import threading
import sys
import json
from battleship import Battleship


class Server:
    def __init__(self):
        self.game = Battleship(boardsize=5, max_ships=2, loaded=False)
        self.game.add_ships('P1', ['a1', 'b2'])
        self.game.add_ships('P2', ['a1', 'b3'])
        self.habilitado = False  # False juega player 1

        self.host = "localhost"
        self.port = 1234
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(2)
        print("Servidor escuchando en {}:{}...".format(self.host, self.port))

        thread = threading.Thread(target=self.accept_connections_thread, daemon=True)
        thread.start()
        print("Servidor aceptando conexiones...")
        self.jugadores = {}
        self.sockets = {"jugador_1": None, "jugador_2": None}

    def accept_connections_thread(self):
        while True:
            client_socket, _ = self.socket_servidor.accept()

            # Luego, como el juego se trata de solo dos jugadores, entonces
            # guardamos solo 2 sockets
            if len(self.jugadores) == 0:
                self.jugadores[client_socket] = 'jugador_1'
                self.sockets["jugador_1"] = client_socket
            elif len(self.jugadores) == 1:
                self.jugadores[client_socket] = 'jugador_2'
                self.sockets["jugador_2"] = client_socket

            print("Servidor conectado a un nuevo cliente...")

            self.listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            self.listening_client_thread.start()

            if len(self.jugadores) == 2:
                msg_jug_1 = {"status": "te_toca",
                             "data": self.game.view_from("P1")}
                msg_jug_2 = {"status": "no_te_toca",
                             "data": self.game.view_from("P2")}
                self.send(msg_jug_1, self.sockets["jugador_1"])
                self.send(msg_jug_2, self.sockets["jugador_2"])
                break

    def listen_client_thread(self, client_socket):
        while True:

            response_bytes_length = client_socket.recv(4)
            print("recibe")
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")

            response = bytearray()

            while len(response) < response_length:
                response += client_socket.recv(256)

            response = response.decode()

            decoded = json.loads(response)

            # Para evitar hacer muy largo este método, el manejo del mensaje se
            # realizará en otro método
            self.handle_command(decoded, client_socket)

    # Los json tiene la forma {'status': % , 'data': %}
    def handle_command(self, received, client_socket):
        #print(received)
        if received["status"] == "ataque":
            if self.jugadores[client_socket] == "jugador_1":
                self.game.attack("P1", received["data"])
                msg_jug_1 = {"status": "no_te_toca",
                             "data": self.game.view_from("P1")}
                msg_jug_2 = {"status": "te_toca",
                             "data": self.game.view_from("P2")}
            elif self.jugadores[client_socket] == "jugador_2":
                self.game.attack("P2", received["data"])
                msg_jug_1 = {"status": "te_toca",
                             "data": self.game.view_from("P1")}
                msg_jug_2 = {"status": "no_te_toca",
                             "data": self.game.view_from("P2")}
        elif received["status"] == "exit":
            msg_jug_1 = {"status": "exit", "data": "Un jugador se salio"}
            msg_jug_2 = {"status": "exit", "data": "Un jugador se salio"}

        print(self.game.game_over())
        if self.game.game_over():
            ganador = self.game.get_winner()
            if ganador == "P2":
                msg_jug_1 = {"status": "termino", "data": "El ganador es el "
                                                          "jugador 2"}
                msg_jug_2 = {"status": "termino", "data": "El ganador es el "
                                                          "jugador 2"}

            elif ganador == "P1":
                msg_jug_1 = {"status": "termino", "data": "El ganador es el "
                                                          "jugador 1"}
                msg_jug_2 = {"status": "termino", "data": "El ganador es el "
                                                          "jugador 1"}

        self.send(msg_jug_1, self.sockets["jugador_1"])
        self.send(msg_jug_2, self.sockets["jugador_2"])
        if not self.habilitado:
            self.habilitado = True
        else:
            self.habilitado = False


    @staticmethod
    def send(value, socket):
        msg_json = json.dumps(value)
        msg_bytes = msg_json.encode()

        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        socket.send(msg_length + msg_bytes)


if __name__ == "__main__":
    serv = Server()
    while True:
        pass






