import socket


def server():
    server = socket.socket()
    server.bind(("localhost", 5555))
    server.listen()

    print("waiting for connection")

    conn, addr = server.accept()
    print("connected....")

    while True:
        msg = conn.recv(1024).decode()
        print(f"Friend: {msg}")
        reply = input("You: ")
        conn.send(reply.encode())


# After receiving the first msg the host will reply
# To receive the msg we need to decode this and to send encode()
