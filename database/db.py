import mysql.connector
from mysql.connector import Error

# Open database connection
def connect():
    db = mysql.connector.connect(host = "localhost", database = "nids", user = "root", password = "Snuffel12")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    return cursor, db

def hashQuery(username):
    cursor,db = connect()
    cursor.execute("SELECT hash FROM Admin WHERE name = %s", (username,))
    hash = str(cursor.fetchall())
    hash = hash.replace('(','').replace(',','').replace(')','').replace("'","").replace('[','').replace(']','')
    db.close()
    return hash

def urlQuery():
    cursor,db = connect()
    cursor.execute("SELECT id,url FROM Weblink")
    urllist = dict(cursor.fetchall())
    db.close()
    return urllist

def desktopQuery():
    cursor,db = connect()
    cursor.execute("SELECT id,mac FROM Desktop")
    desklist = dict(cursor.fetchall())
    db.close()
    return desklist

def mailQuery():
    cursor,db = connect()
    cursor.execute("SELECT id,mail,name FROM Email")
    maillist = dict(cursor.fetchall())
    db.close()
    return maillist

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Selector for UI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def selector(dict):
    if dict["func"] == "newDesk":
        newDesk(dict)
    if dict["func"] == "newMail":
        newMail(dict)
    if dict["func"] == "newUrl":
        newUrl(dict)
    if dict["func"] == "dropDesk":
        dropDesk(dict)
    if dict["func"] == "dropMail":
        dropMail(dict)
    if dict["func"] == "dropUrl":
        dropUrl(dict)

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Desk for UI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def newDesk(dict):
    id = dict["ID"]
    mac = dict["MAC"]
    cursor,db = connect()
    cursor.execute("INSERT INTO Desktop (id, mac) VALUES (%s, %s)",(id, mac,))
    db.commit()
    db.close()

def dropDesk(dict):
    id = dict["ID"]
    cursor,db = connect()
    cursor.execute("DELETE FROM Desktop WHERE id = %s", (id,))
    db.commit()
    db.close()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Mail for UI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def newMail(dict):
    name = dict["name"]
    mail = dict["mail"]
    cursor,db = connect()
    cursor.execute("INSERT INTO Email (mail, name ) VALUES (%s, %s)",(mail, name,))
    db.commit()
    db.close()

def dropMail(dict):
    mail = dict["mail"]
    cursor,db = connect()
    cursor.execute("DELETE FROM Email WHERE mail = %s", (mail,))
    db.commit()
    db.close()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ URL for UI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def newUrl(dict):
    url = dict["URL"]
    cursor,db = connect()
    cursor.execute("INSERT INTO Weblink (url) VALUES (%s)", (url,))
    db.commit()
    db.close()

def dropUrl(dict):
    url = dict["URL"]
    cursor,db = connect()
    cursor.execute("DELETE FROM Weblink WHERE url = %s", (url,))
    db.commit()
    db.close()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Test dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
thisdict =	{
    "func": "newUrl",
    "mail": "snuffelsnuffel76@gmail.com",
    "name": "Mailserver"}
