import socket
import threading
from rsa import RSA

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

rsa = RSA()

# receive e and N and d from server
keys = client.recv(1024).decode().split(",")
e = int(keys[0])
N = int(keys[1])
d = int(keys[2])
# override with server's keys
rsa.e = e
rsa.N = N
rsa.d = d


def receive(client):
    while True:
        try:
            msg = client.recv(65536).decode()
            ciphertext = list(map(int, msg.split(",")))
            msg = rsa.decrypt(ciphertext)  # decrypt with server's d
            print(msg)
        except:
            print(f"Error: {e}")
            break


def send(client):
    name = input("What is your name: ")
    while True:
        try:
            msg = input()
            encrypted = rsa.encrypt(f"[{name}]: {msg}")
            encrypted_str = ",".join(map(str, encrypted))
            client.send(encrypted_str.encode())
        except:
            break


t1 = threading.Thread(target=receive, args=(client,))
t2 = threading.Thread(target=send, args=(client,))
t1.start()
t2.start()
