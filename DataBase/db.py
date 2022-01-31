#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    * Database program for control our access point.
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman

"""

"""
Libraries
"""

import sqlite3 as lite


"""
Code
"""

def setup():
    """
    Create a database called siscom.db with a single table with the users' macs, entry time, exit time and status (connected/disconnected)
    """

    con = lite.connect('siscom.db')
    cur = con.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS USUARIS;
    CREATE TABLE USUARIS
        (
        mac CHAR[20] NOT NULL PRIMARY KEY,
        hora_entrada DATE NOT NULL,
        hora_sortida DATE NOT NULL,
        estat INTEGER NOT NULL
	);

    """)
    con.commit()

setup()
