import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        try:
            while True:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(message)
                    if "name" in message:
                        name = input("Enter your name: ").strip()
                        self.client_socket.send(name.encode())
                    if "Choose" in message:
                        choice = input("Your choice: ").strip()
                        self.client_socket.send(choice.encode())
                    elif "final_result" in message:
                        break

        except KeyboardInterrupt:
            print("\n[*] Connection closed.")
            self.client_socket.close()
        except Exception as e:
            print(f"Error: {e}")
            self.client_socket.close()


if __name__ == "__main__":
    client = Client('127.0.0.1', 8100)
    client.connect()
