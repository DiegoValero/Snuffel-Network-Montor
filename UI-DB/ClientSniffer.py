import socket
import sys
import pickle

# This function puts the packet in a dict with a packet id.


def get_http(payload, id, MAC, IP):
    packet_check = {"id": id, "payload": payload, "MAC": MAC, "IP": IP}
    return send(packet_check)

def get_mail():# NEW
    packet = {"id": "getmail"}# NEW
    return send(packet)# NEW

# This function used pickle to send the packet towards the database.
# If it receives a dict it will return the packet if the dict contains a url.


def send(packet_check):
    try:
        message = pickle.dumps(packet_check)
        s.sendall(message)
        data = s.recv(1024)
        packet = pickle.loads(data)
        if packet["id"] == "getmail":# NEW
            return packet# NEW
        elif packet["url"] != "":
            return packet
        else:
            return 0

    except socket.error:
        print("Error! {}".format(socket.error))
        exit()


# This is the part where the sniffer connects with the database.
HOST = 'localhost'
PORT = 1234
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()
print("Connection succeeded.")
