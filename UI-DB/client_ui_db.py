import socket
import sys
import pickle

def send(packet):
    try:
        print(packet)
        message = pickle.dumps(packet)
        s.sendall(message)
        data = s.recv(1024)
        packet = pickle.loads(data)
        print(packet)

    except socket.error:
        print("Error! {}".format(socket.error))
        exit()


# This is the part where the sniffer connects with the database.
HOST = '145.109.179.0'
PORT = 1235
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()
print("Connection succeeded.")
