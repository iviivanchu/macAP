# coding: utf-8
# #!/usr/bin/python

"""
    * Server Web program for provide a web interface to be able to control and manage our access point.
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman

"""

"""
Libraries
"""

from flask import Flask



"""
Code
"""

app = Flask(__name__)

from routes import *

app.run(host="0.0.0.0", port = 5000)    #Server running in port 5000. 
