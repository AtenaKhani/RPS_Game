import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.names = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f" Listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f" Accepted connection from {addr}")
            task = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
            task.start()

    def handle_client(self, client_socket):
        self.clients.append(client_socket)
        client_socket.send("Hi, welcome to the game. Please enter your name: ".encode())
        while True:
            name = client_socket.recv(1024).decode().strip()
            if name in self.names:
                client_socket.send("This name is already taken. Please choose a different name.".encode())
            else:
                self.names.append(name)
                break
        if len(self.names) == 2:
            for client_socket in self.clients:
                client_socket.send("Game is starting!".encode())
            self.play_game()

    def specify_winner(self, choices):
        wins_mode = {
            "r": "s",
            "p": "r",
            "s": "p"
        }
        choice1, choice2 = choices
        if choice1 == choice2:
            return 0
        elif choice2 == wins_mode[choice1]:
            return 1
        else:
            return 2
