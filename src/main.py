from Interface import ChatWindow
from ChatReader import ChatBot
from Tokens import Datos

nickname = Datos.NICKNAME
token = Datos.TOKEN
channel = Datos.CHANNEL
server = Datos.SERVER
port = Datos.PORT

if __name__ == "__main__":
    ventana = ChatWindow()
    bot = ChatBot(nickname, token, channel, ventana, server, port)
    ventana.run()