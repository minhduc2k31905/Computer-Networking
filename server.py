import json
import socket
import threading
import sys

from client import order

HOST = "127.0.0.1"
PORT = 12344

list_client = []
list_Customer = {}


def accept_connections():
    global list_Customer
    readCustomer()

    while True:
        client, adr = ser.accept()
        print(f"Connected to {adr}")
        client.sendall(
            "------ Welcome to Ruki Food Store ------".encode("utf8"))
        # receive name
        nick = client.recv(1024).decode("utf8")
        list_client.append(client)

        # mess in client
        client.sendall(
            "You are connected to our store. Let's order now".encode("utf8"))
        print(f"{nick} has come to order")

        threading.Thread(target=handle, args=(client, nick,)).start()


def readCustomer():
    # receive data of previous customers
    global list_Customer
    with open('cus.json', 'r') as f:
        data = json.loads(f.read())
    list_Customer = data.copy()


def handle(client, nick):
    global list_Customer
    # Send menu
    with open("menu.json", 'r') as f:
        data = json.loads(f.read())
    # convert dict to strings
    menu = json.dumps(data)
    client.sendall(menu.encode("utf8"))

    # check if user has order before
    ordered = False
    for x in list_Customer:
        if nick == list_Customer[x]["name"]:
            ordered = True
            print("used to order")
            client.sendall("ordered".encode('utf8'))
            info = json.dumps(list_Customer[x])
            client.sendall(info.encode('utf8'))

    if ordered == False:
        print("not order before")
        client.sendall("not ordered".encode('utf8'))

    # =========== receive customer's order
    mess = client.recv(1024).decode('utf8')
    data = client.recv(1024).decode('utf8')
    customer = json.loads(data)
    if mess == "update":
        # update customer["nick"]
        for x in list_Customer:
            if nick == list_Customer[x]["name"]:
                list_Customer[x] = customer
            pass
    else:
        # append customer["nick"]
        list_Customer.update({nick: customer})

    # write to file customer.json
    data = json.dumps(list_Customer, indent=2)
    with open("cus.json", 'w') as file:
        file.write(data)

    list_client.remove(client)
    print(f"{nick} has left the store")
    client.close()


if __name__ == "__main__":
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        ser.bind((HOST, PORT))
    except:
        print("Bind failed. Error: " + str(sys.exc_info()))
        sys.exit()

    ser.listen(6)   # Queue up to 5 requests
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()
