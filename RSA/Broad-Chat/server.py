import socket
import threading
from rsa import RSA

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5555))
server.listen()

rsa = RSA()  # one RSA instance for everyone!
clients = []


def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                clients.remove(client)


def handleClients(conn, addr):
    print(f"[+] {addr} connected.")

    # send e and N to the new client so they can encrypt
    conn.send(f"{rsa.e},{rsa.N},{rsa.d}".encode())
    clients.append(conn)
    while True:
        try:
            msg = conn.recv(65536).decode()
            if not msg:
                break
            print(f"[{addr}] {msg}")
            broadcast(msg, conn)
        except:
            break
    clients.remove(conn)
    conn.close()
    print(f"[{addr}] disconnected.")


while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handleClients, args=(conn, addr))
    thread.start()
