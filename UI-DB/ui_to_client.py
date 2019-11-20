from client_ui_db import send

# Version 1.0
# Made by: Jacintha Walters
# Fetches all the information that is needed for the UI.

# Type is request and table declares which table.
def request(table):
    dict = {"type": "req", "table": table}
    send(dict)
    return 0

# Type is request, table is hash and the username is the username
# required to fetch the hash.
def requestHash(table, username):
    dict = {"type": "req", "table": table, "username": username}
    send(dict)
    return 0

# Type is drop, table declares from which table, toDrop is which value
# and the id is the id of the value.
def drop(table, value, id):
    dict = {"type": "drop", "table": table, "toDrop": value, "id": id}
    send(dict)

# Insert to the table with a certain value and id (if needed).
def insert(table, value, id):
    dict = {"type": "insert", "table": table, "toInsert": value, "id": id}
    send(dict)

# Requests with the right table to send.
mails = request("Mail")
subnet = request("Subnet")
desktops = request("Desktop")
admins = requestHash("Admin", "admin1")
weblink = request("Weblink")
