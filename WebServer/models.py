# coding: utf-8
# #!/usr/bin/python

"""
    * File to interact with database.
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman

"""

"""
Libraries
"""

import sqlite3

"""
Global variables
"""

database ="/home/ivan/Documentos/SisComAP/DataBase/siscom.db"        # Database file path. 
                                                                                       # IMPORTANT:
                                                                                       #  - Change the path, according to the computer where it is executed.
                                                                                       #  - First you have to create the database with 'python3 db.py' in Database directory.

"""
Code
"""

def insert_mac(mac, hora_entrada, hora_sortida, estat):
    """
    Insert user in database. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("INSERT INTO USUARIS (mac, hora_entrada, hora_sortida, estat) VALUES ((?),(?),(?),(?))", (mac, hora_entrada, hora_sortida, estat,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def check_all():
    """
    Returns 'USUARIS' table. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM USUARIS")
        mac = cur.fetchall()
        conn.close()
        return mac

    except Exception as e:
        print (e)
        return -1


def check_mac(mac):
    """
    Returns the characteristics of a user with a mac. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM USUARIS WHERE mac = (?)", (mac,))
        mac = cur.fetchone()
        conn.close()
        return mac

    except Exception as e:
        print (e)
        return -1


def check_horaEntrada(mac):
    """
    Returns the login time of a user with a MAC. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT hora_entrada FROM USUARIS WHERE mac = (?)", (mac,))
        mac = cur.fetchall()
        conn.close()
        return mac

    except Exception as e:
        print (e)
        return -1


def check_horaSortida(mac):
    """
    Returns the exit time of a user with a MAC.  On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT hora_sortida FROM USUARIS WHERE mac = (?)", (mac,))
        mac = cur.fetchall()
        conn.close()
        return mac

    except Exception as e:
        print (e)
        return -1


def check_state(mac):
    """
    Returns user state. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT estat FROM USUARIS WHERE mac = (?)", (mac,))
        mac = cur.fetchall()
        conn.close()
        return mac

    except Exception as e:
        print (e)
        return -1


def update_state(estat, mac):
    """
    Update user state. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("UPDATE USUARIS SET estat = (?) WHERE mac = (?)", (estat, mac,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def update_horaEntrada(hora_entrada, mac):
    """
    Update login time to user. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("UPDATE USUARIS SET hora_entrada = (?) WHERE mac = (?)", (hora_entrada, mac,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def update_horaSortida(hora_sortida, mac):
    """
    Update exit time to user. On error, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("UPDATE USUARIS SET hora_sortida = (?) WHERE mac = (?)", (hora_sortida, mac,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def delete_mac(mac):
    """
    Deletes user. On errro, report and return -1.
    """

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM USUARIS WHERE mac = (?)",(mac,))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return -1
