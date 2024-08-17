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

    def play_game(self):
        player1_wins = 0
        player2_wins = 0
        rounds = 3
        for _ in range(rounds):
            choices = [None, None]
            threads = []
            for i, client_socket in enumerate(self.clients):
                thread = threading.Thread(target=self.get_choice, args=(client_socket, choices, i))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            winner = self.specify_winner(choices)
            result = "No one won!" if not winner else f"{self.names[0] if winner == 1 else self.names[1]} wins this round!"
            if winner == 1:
                player1_wins += 1
            elif winner == 2:
                player2_wins += 1
            for client_socket in self.clients:
                client_socket.send(result.encode())

        final_result = "final_result:It's a tie!" if player1_wins == player2_wins else f"final_result:{self.names[0] if player1_wins > player2_wins else self.names[1]} wins the game!"
        for client_socket in self.clients:
            client_socket.send(final_result.encode())

    def get_choice(self, client_socket, choices, index):
        while True:
            client_socket.send("Choose 'r:rock', 'p:paper', or 's:scissors': ".encode())
            choice = client_socket.recv(1024).decode().strip().lower()
            if choice in ['r', 'p', 's']:
                choices[index] = choice
                break
            else:
                client_socket.send("Invalid choice. Please choose 'r', 'p', or 's'.".encode())

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


if __name__ == "__main__":
    server = Server('127.0.0.1', 8100)
    server.start()
