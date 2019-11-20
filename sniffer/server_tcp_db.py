import socket
import pickle
from db import url

# Looks for a TCP connection with a host.
HOST = '145.109.155.130'
PORT = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print("Connection succeeded.")

# For every package it checks if a link inside the database matches.
# Per package one response is send back, an empty url means the package doesn't match
# and if a url is found the url will be send back.
while 1:
    data = conn.recv(1024)
    if not data:
        break
    packet = pickle.loads(data)
    payload = packet["payload"]
    link = url()
    url_found = ""
    for i, ding in link.items():
        url_bool = 0
        if payload.find(ding.encode()) != -1:
            url_bool = 1
            url_found = ding

        else:
            continue
    packet_resp = {"id": packet["id"], "url" : url_found}
    message = pickle.dumps(packet_resp)
    conn.send(message)
