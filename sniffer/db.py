import mysql.connector
from mysql.connector import Error

# Connects to the database and fetches all the urls inside a dict then returns it.

def url():
    db = mysql.connector.connect(host = "localhost", database = "nids", user = "root", password = "HondenBrok5" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT id,url FROM Weblink")

    # Fetch a single row using fetchone() method.

    data = dict(cursor.fetchall())

    # disconnect from server
    db.close()
    return data

url()
