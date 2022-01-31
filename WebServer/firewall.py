# coding: utf-8
# #!/usr/bin/python


"""
    * Firewall for control users in our acces point
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman

"""


"""
Libraries
"""

import subprocess                                # For interact with OS.
from threading import Timer, Thread, Event       # For throw  timer threads.
import models                                    # For interact with database.
import datetime                                  # For time.
from time import sleep                           # For time.
import scan                                      # For obtain IP and MAC from devices. Also, lets you know the status of client


"""
Code
"""


class Scheduler():
    """
    Implement a software sheduler using timer threads and run a handler when the event occurs.
    """

    def __init__(self, t, hFunction, args = None, bucle = False):
        """
        Initialize the Scheduler class.
        """

        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)
        self.bucle = bucle
        self.args = args


    def handle_function(self):
        """
        Executes the / handle function indefinitely or once by throwing a timer thread.
        """

        if self.bucle:                                            # If bucle is actived
            if self.args == None:
                self.hFunction()
            else:
                self.hFunction(self.args)
            self.thread = Timer(self.t, self.handle_function)      # Start timer thread. When the thread time runs out the function is executed
            self.thread.start()
        else:
            if self.args == None:
                self.hFunction()
            else:
                self.hFunction(self.args)


    def cancel(self):
        """
        Cancels the execution of a timer thread, and therefore does not execute the handle.
        """

        self.thread.cancel()



    def start(self):
        """
        Initialize a timer thread.
        """
        self.thread.start()



class Control(object):
    """
    Set up a firewall through timer threads that interacts with the database to access or remove clients from the access point according to their assigned hours.
    """

    def __init__(self):
        """
        Initialize the class. At the time of creating the class a timer thread is launched 
        which will run every second and execute the control function. When creating an instance 
        of the control class, uwf is enabled as a firewall (so no traffic is allowed).
        """

        self.users = {}                                   # Contains threads timer of users.
        self.connected  = {}                              # Users connected in AP.
        sh = Scheduler(1,self.control,bucle=True)         # Run every second control function. 
        sh.start()                                        
        subprocess.call(["sudo","ufw","enable"])          # Firewall is enable. In this moment, no traffic is allowed.


    def disconnect(self, args):
        """
        This function is executed once a user's time has elapsed. 
        If it was connected, it removes it from the connected list and the timer thread list. 
        On the other hand, it denies traffic to this user.
        """

        ip = args[1]                                           # User IP
        mac = args[0]                                          # User MAC 
        print("FINISH THREAD FOR USER", mac, ", IP:",ip)       # Reports that the user's time with mac 'mac' has expired.
        if mac in self.users:                                  # If user is connected now
            del self.users[mac]                                # Delete user

        if mac in self.connected:                              # Deletes user if is connected
            del self.connected[mac]

        models.update_state(0,mac)                             # Update database state for user.
        #print("USUARIS:",self.users)                          # Debug
        subprocess.call(["sudo","ufw","deny","from",ip])       # It denies traffic to the user because it is out of time.


    def delete(self,mac):
        """
        Delete a user. If it is connected, it removes it from the connected list and denies traffic.
        """

        arp_connected = scan.read_MAC()                                             # Checks users avaible.
        user = models.check_mac(mac)

        if mac in self.users:                              
            self.users[mac].cancel()                                                # Cancel timer thread, if it exists.
            del self.users[mac]                                             

        if mac in self.connected:
            del self.connected[mac]

        if mac in arp_connected: 
            subprocess.call(["sudo","ufw","deny","from",arp_connected[mac]])        # Deny traffic for user.
        print("USER",mac,"DELETE")                                                  # Reports that the user's is deleted.


    def cancel(self, mac):
        """
        If a user logs out and was logged in, their status in the database changes. 
        It is also deleted from the list of connected users.
        """

        if mac in self.connected:                # If user was connected
            del self.connected[mac]              # Cleats the connected users

        models.update_state(0, mac)              # Updates database state for the user.          
        print ("USER", mac, "DISCONNECT")        # Informs the users is disconnect


    def get_connected(self):
        """
        Returns users connected.
        """

        return self.connected


    def modify(self, mac):
        """
        It allows to modify parameters of a user for the firewall.
        """

        hora = datetime.datetime.strptime(day_hour(), "%H:%M")
        arp_connected = scan.read_MAC()
        user = models.check_mac(mac)
        hora_in = datetime.datetime.strptime(user[1], "%H:%M")
        hora_out = datetime.datetime.strptime(user[2], "%H:%M")

        if hora_in <= hora and hora < hora_out:

            if mac in self.users:                                                   # If user is connected and new time of exit is after and login time is before.
                print("RECONFIGURE TIME")                                           # Informs that time is reconfigured.
                total_time = hora_out - hora                                   
                totalTime_sec = int(total_time.total_seconds())                     # Recalculte new time.
                self.users[mac].cancel()
                del self.users[mac]
                self.users[mac] = Scheduler(totalTime_sec, self.disconnect, args = (mac, arp_connected[mac]), bucle = False)   # Start new timer thread with new hours.
                self.users[mac].start()

        else:                                                                       # If it is not in your range of hours
            print("ACCES DENIED")                                                   # Informs thats acces is denied
            subprocess.call(["sudo","ufw","deny","from",arp_connected[mac]])        # Denied traffic for user

            if mac in self.users:                              
                self.users[mac].cancel()                                            # Delete timer threads if are exist.
                del self.users[mac]                              

            if mac in self.connected:
                del self.connected[mac]                                             
                models.update_state(0, mac)                                         # Change your status to disconnected in the database.


    def control(self):
        """
        It runs every second and checks the database if there is any user 
        that has permissions to use the access point. If so, access is allowed 
        through the firewall and then a timer thread is launched that will not allow traffic once the timer has expired.
        If a user disconnects, it also detects it and cancels the timer threads it has. 
        It also controls the reconnection of users.
        It informs about all the movements that happen in the system.
        """

        hora = datetime.datetime.strptime(day_hour(), "%H:%M")                             # Current time
        users = models.check_all()                                                         # Obtain all users from database.
        arp_connected = scan.read_MAC()                                                    # Checks users avaibles by ARP scan.

        for i in users:
            hora_in = datetime.datetime.strptime(i[1], "%H:%M")
            hora_out = datetime.datetime.strptime(i[2], "%H:%M")

            if (hora_in <= hora and hora < hora_out):

                if i[0] in arp_connected:                           

                    client_connected = scan.isConnected(arp_connected[i[0]])                        # Checks if user is connected sends ICMP (ping) packet.

                    if i[0] not in self.users and i[0] not in self.connected and client_connected:  # If the user is online and within their hour for the first time
                        print ("ACCES PERMES USUARI", i[0])                                         # Informs that the traffic is allowed to the user.
                        print("CLIENT", i[0], "CONNECTED")                                          # Informs that user with mac 'mac' is connected.
                        subprocess.call(["sudo","ufw","allow","from",arp_connected[i[0]]])          # Traffic is allowed.
                        self.connected[i[0]] = True                                                 # User in list of connected.
                        self.users[i[0]] = Scheduler(get_time(i[1], i[2]), self.disconnect, args = (i[0], arp_connected[i[0]]), bucle = False)  # It will disconnect the user once the assigned time expires
                        self.users[i[0]].start()                                                    
                        models.update_state(1, i[0])                                                # Change your status to connected in the database.

                    elif i[0] in self.users and i[0] in self.connected and not(client_connected):   # If the user logs out
                        self.cancel(i[0])

                    elif i[0] in self.users and i[0] not in self.connected and client_connected:    # If the user reconnects
                        print("CLIENT", i[0], "RECONNECTED")                                        # Inform that user is reconnect.
                        self.connected[i[0]] = True                                                 # User in list of connected.
                        models.update_state(1, i[0])                                                # Change your status to connected in the database.


"""
Aditional Functions
"""

def get_time(time_in,time_out):
    """
    Returns the time in seconds between a start date and an end date. 
    This time will be used to launch the timer threads.
    """

    hora_in = datetime.datetime.strptime(time_in, "%H:%M")
    hora_out =  datetime.datetime.strptime(time_out, "%H:%M")

    substract = hora_out - hora_in
    new_substract = int(substract.total_seconds())

    return new_substract


def day_hour():
    """
    Returns the current date and time in the database format.
    """

    hora = datetime.datetime.now().strftime("%H:%M")
    return hora
