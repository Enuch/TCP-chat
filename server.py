from concurrent.futures import thread
from email import message
import threading
import socket

host = 'localhost'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nickNames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickName = nickNames[index]
            broadcast(f'{nickName} saiu do chat'.encode('ascii'))
            nickNames.remove(nickName)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Conectado com {str(address)}')
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nickNames.append(nickname)
        clients.append(client)
        
        print(f'Nome do cliente é {nickname}|')
        broadcast(f'{nickname} entrou no chat!'.encode('ascii'))
        client.send('Conectado ao server!'.encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
print("Servidor ligado!")
receive()