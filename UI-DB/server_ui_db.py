import socket
import pickle
import db


# Looks for a TCP connection with a host.
HOST = '145.109.179.0'
PORT = 1235
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print("Connection succeeded.")

def unpack(packet):
    if packet["type"] == "req":
        if packet["table"] == "Mail":
            return db.mailQuery()
        elif packet["table"] == "Desktop":
            return db.desktopQuery()
        elif packet["table"] == "Subnet":
            return db.subQuery()
        elif packet["table"] == "Admin":
            return db.hashQuery(packet["username"])
        elif packet["table"] == "Weblink":
            return db.urlQuery()
        else:
            return "error"

    elif packet["type"] == "insert":
        if packet["table"] == "Desktop":
            db.newDesk(packet["id"], packet["toInsert"])
            return 0
        elif packet["table"] == "Mail":
            db.newMail(packet["id"], packet["toInsert"])
            return 0
        elif packet["table"] == "URL":
            db.newUrl(packet["toInsert"])
            return 0
        else:
            return("error")

    # Returned 1 als het toevoegen succesvol ging
    elif packet["type"] == "drop":
        if packet["table"] == "Desktop":
            db.dropDesk(packet["id"])
            return 0
        elif packet["table"] == "Mail":
            db.dropMail(packet["toDrop"])
            return 0
        elif packet["table"] == "URL":
            db.dropUrl(packet["toDrop"])
            return 0
        else:
            return "error"

while 1:
    data = conn.recv(1024)
    if not data:
        break
    packet = pickle.loads(data)
    print(packet)
    message = unpack(packet)
    print(message)
    message_b = pickle.dumps(message)
    conn.send(message_b)
