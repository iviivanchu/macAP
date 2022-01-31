
# Configurable Wi-Fi AP

The main objective of this project is to create an access point and control the users who connect through the MAC, with the option of denying entry to users who are not on a list of interest and even being able to expel to users who are already connected if they are not in the range of hours that it is up to.





## Configuration Manual

#### First step

For the creation of the AP we will use graphical application nm-connection-editor, which is already pre-installed in Ubuntu. Once in the app, we add a new connection, where we define an SSID, select access point mode, and determine our wi-fi network interface. In wireless security, we select the type of security WPA and WPA2 and we will put a password.

Once created what we have to do is activate it, for this in the Ubuntu wireless configuration there is an option where it allows you to activate the wireless access point, all we have to do is put the name of the connection and the password of the connection that we have created for the access point, and our pc will enter access point mode. 

#### Second step

Create the database by running python3 db.py in the DataBase directory

```
  python3 db.py
```

#### Third step

Change the path of the database file in the models.py file in the WebServer directory. To change it run pwd in the DataBase directory and paste the output + '/siscom.db' into the database variable of the models.py  file.

#### Third step

Change the path of the database file in the models.py file in the WebServer directory. To change it run pwd in the DataBase directory and paste the output + '/siscom.db' into the database variable of the models.py  file.

#### Fourth step

Run the main server program withsudo python3 __init__.py in the WebServer directory.

```
  sudo python3 __init__.py
```
