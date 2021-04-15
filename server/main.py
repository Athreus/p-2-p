import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []


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
            clients.close()
            name = names[index]
            broadcast(f'{name} left the chat.'.encode('ascii'))
            names.remove(name)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connection Established with {}".format(str(address)))

        client.send('BRUH'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        print("Name of the client is {}".format(name))
        broadcast("{} joined the chat.".format(name).encode('ascii'))
        client.send('Connected to the server.'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server is listening..")
receive()