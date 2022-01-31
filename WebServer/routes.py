# -*- coding: utf-8 -*-


"""
    * Routes program for Server Web program to provide the routes for the website to be able to control and manage our access point.
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman

"""


"""
Libraries
"""

from flask import *
from flask import Blueprint, render_template, request, redirect, Response, url_for
import datetime
import models
import firewall


"""
Global variables
"""

app = Flask(__name__)                       # Flask instance.
users_connected = {}                        # Users connected to our acces point.
firewall = firewall.Control()               # Firewall instance for control/interact with our firewall and time threads system.


"""
Code
"""


@app.route("/", methods=["GET", "POST"])
def index():
   """
   Provides the login page when the resource is requested. On the other hand, if the input form is filled, 
   it checks if the data is correct and if so, it renders the main admin page. In case the input data to 
   the input form is incorrect, an error is returned.
   """

   if (request.method == "POST"):
      user = request.form["textUser"]
      password = request.form["inputPassword"]

      if user.upper() == "ADMIN" and password.upper() == "ADMIN":       # Checks values of form.
         users = []                                                     # Users list in system. 
         all_users = models.check_all()                                 # Users avaibles in database.

         for i in all_users:                                            # Checks state for all users in system  and puts in list users.
            if not(i[3]):
               users.append([i[0],"DISCONNECT"])
            else:
               users.append([i[0],"CONNECT"])
               
         if all_users == []:                                            # If there are no users, it returns the string "---" to indicate that there are no users created.
            users.append(["---","---"])         
         return render_template("admin.html", users = users)            # Returns template 'admin.html' with users list avaible in system. 

      else:
         return render_template("login.html", error = True)             # Returns error if credentials are incorrect.


   else:                                                                # If request method is 'GET' returns login page. 
      return render_template("login.html")



@app.route("/admin", methods=["GET"])
def admin():
   """
   Render the main page of the website administrator.
   """

   users = []                                                           # Users list in system. 
   all_users = models.check_all()                                       # Users avaibles in database.
  
   for i in all_users:
      if not(i[3]):
         users.append([i[0],"DISCONNECT"])
      else:
         users.append([i[0],"CONNECT"])

   if users == []:                                                      # If there are no users, it returns the string "---" to indicate that there are no users created.
      users.append(["---","---"])
   return render_template("admin.html", users = users)



@app.route("/create",methods=["GET", "POST"])
def create():
   """
   Create a new user to be connected to our access point in a time interval. 
   If the user's MAC does not already exist in the database, it will report the error. 
   On the other hand, if the times are incorrect, it will also report an error. 
   If the data entered is correct, it is entered into the database.
   """

   if (request.method == "POST"):                                           # If the form is filled and request method is POST.
     mac = request.form["UserName"]
     data_input = request.form["data-input"]
     data_output = request.form["data-output"]

     new_data_input = datetime.datetime.strptime(data_input, "%H:%M")       # Convert time in database format.
     new_data_output = datetime.datetime.strptime(data_output, "%H:%M")     # Convert time in database format.

     find_mac = [i[0] for i in models.check_all()]                          # Checks if MAC exists

     if mac not in find_mac :
        if new_data_input > new_data_output:
            return render_template("create.html", msg = "dataInvalid")      # Returns error if data is invalid.
        else:
            models.insert_mac(mac,data_input,data_output, 0)                # If information are correct, insert data in database.
            return render_template("create.html", msg = "created")        

     else:
        return render_template("create.html", msg = "userExist")            # Reports that the user already exists.

   else:                                                                    # If request method is GET, returns page to create user.
     return render_template("create.html")



@app.route("/reconfigure", methods=["GET", "POST"])
def reconfigure():
   """
   Reconfigures the entry and exit times of a user.
   In case of error in the hours it shows the error. 
   On the other hand, if the user does not exist, it reports that it does not exist.
   Insert correct data in database to reconfigure.
   """

   if (request.method == "POST"):                                                 # If form is completed and request method is POST.
     mac = request.form["UserName"]
     data_input = request.form["data-input"]
     data_output = request.form["data-output"]

     new_data_input = datetime.datetime.strptime(data_input, "%H:%M")             # Convert time in database format.
     new_data_output = datetime.datetime.strptime(data_output, "%H:%M")           # Convert time in database format.

     find_mac = [i[0] for i in models.check_all()]                                # Checks if MAC exists

     if mac in find_mac:
        if new_data_input > new_data_output:
            return render_template("reconfigure.html", msg = "dataInvalid")       # Returns error if data is invalid.
        else:
            models.update_horaEntrada(data_input, mac)                            # If information are correct, update data in database.
            models.update_horaSortida(data_output, mac)                           # If information are correct, update data in database.
            firewall.modify(mac)                                                  # Updates firewall for user.
            return render_template("reconfigure.html",msg = "ok")

     else:
        return render_template("reconfigure.html",msg = "userExist")              # If user not exists, reports error.

   else:                                                                          # If request method is GET, returns reconfigure page.
     return render_template("reconfigure.html")



@app.route("/delete", methods=["GET", "POST"])
def delete():
   """
   Delete a user from our system if it exists. In case of error inform.
   """
   if (request.method == "POST"):                                                 # If form is completed and request method is POST.
     mac = request.form["UserName"]
     find_mac = [i[0] for i in models.check_all()]                                # Checks if MAC exists.

     if mac in find_mac:
        firewall.delete(mac)                                                      # Remove user from firmware.
        models.delete_mac(mac)                                                    # Remove user from database
        return render_template("delete.html", msg = "delete")

     else:
        return render_template("delete.html", msg = "NOdelete")                   # If user not exist, reports error.

   else:                                                                          # If request method is GET, returns delete page.
     return render_template("delete.html")



@app.route("/api/changes", methods=["GET"])
def new_changes():
   """
   Returns the users who have connected and disconnected. 
   This route is accessed through AJAX to dynamically update 
   the web page informing of the changes in the access point.
   """

   content = {}                                     
   users_now = firewall.get_connected()             # Users avaible in acces point now.
   disconnect = []                                  # Users that are disconnected.
   text = ""                                        # Text for show in website.
   
   for i in users_now:                              # First, check if there are new user.
      if i not in users_connected:
         users_connected[i] = True
         text += i+" CONNECTED\n"

   for i in users_connected:                        # After, check if any user are disconnected.
      if i not in users_now:
         disconnect.append(i)
         text += i+ " DISCONNECTED\n"


   for i in disconnect:                             # If user are disconnected, deletes him of list of users connected.
      del users_connected[i]

   if text == "":                                   # If there are not changes, reports him in website.
      text = "No changes yet"

   content["msg"] = text
   #print(content)                                  #Debug
   return content, 200
