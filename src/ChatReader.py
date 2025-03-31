import socket
import ssl
import threading

class ChatBot():
    def __init__(self, NICKNAME, TOKEN, CHANNEL, CHATWINDOW, SERVER, PORT):
        self.nickname = NICKNAME
        self.token = TOKEN
        self.channel = CHANNEL
        self.chatwindow = CHATWINDOW
        self.server = SERVER
        self.port = PORT
        self.running = True
        self.sock = None

        self.connect_irc()

    def connect_irc(self):
        try:
            sock = socket.create_connection((self.server, self.port))
            context = ssl.create_default_context()
            self.sock = context.wrap_socket(sock, server_hostname=self.server)

            self.send_command(f"PASS {self.token}")
            self.send_command(f"NICK {self.nickname}")
            self.send_command(f"JOIN {self.channel}")

            response = self.sock.recv(2048).decode('utf-8')
            print(f"Twitch: {response}")

            if "Login authentication failed" in response:
                print("Authentication failed")
                self.sock = None
                return

            threading.Thread(target=self.listen_for_messages, daemon=True).start()

        except Exception as e:
            print(f"Connection failed: {e}")

    def send_command(self, command):
        if self.sock:
            try:
                self.sock.send(f"{command}\r\n".encode('utf-8'))
            except Exception as e:
                print(f"Command failed:{e}")

    def listen_for_messages(self):
        try:
            while self.running:
                response = self.sock.recv(2048).decode('utf-8')
                
                if response.startswith("PING"):
                    self.send_command("PONG :tmi.twitch.tv")

                if "PRIVMSG" in response:
                    username = response.split("!", 1)[0][1:] 
                    message = response.split("PRIVMSG", 1)[1].split(":", 1)[1]  
                    formatted_message = f"{username}: {message}"

                    if self.chatwindow and self.chatwindow.root:
                        self.chatwindow.root.after(0, self.chatwindow.update_chat, formatted_message)

        except Exception as e:
            print(f"Listen failed: {e}")
            if self.sock:
                self.close_irc()

    def close_irc(self):
            if self.sock:
                self.sock.close()
                self.sock = None