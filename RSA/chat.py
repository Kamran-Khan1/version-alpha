from server import server
from client import client


def main():
    print("Option \n1) Host a server \n2) Become a client")
    user = input()

    if user == "1":
        server()
    elif user == "2":
        client()
    else:
        print("Invalid selection")


if __name__ == "__main__":
    main()
