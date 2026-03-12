import socket


def client():
    client = socket.socket()
    client.connect(("localhost", 5555))

    while True:
        msg = input("You: ")
        client.send(msg.encode())
        reply = client.recv(1024).decode()
        print(f"Friend: {reply}")


# client have to send the message then server or host will receive it
# To send msg we need to encode(), to receive decode()
