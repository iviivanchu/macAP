# -*- coding: utf-8 -*-


"""
    * ARP scanner to see connected and disconnected devices in our AP
    * Comunication system
    * Developed by Ivan Chamero and Manuel Angel Roman

"""


"""
Libraries
"""

import pyping                                      # pip install git+git://github.com/tkuebler/pyping


"""
Code
"""

def read_MAC(): 
    """
    Returns a dictionary with the MACs connected to our system and their IP. 
    To read the values, we access the /proc/net/arp file of the operating system.
    """

    arp_file = open("/proc/net/arp", "r", encoding = "utf-8-sig")

    line = 0
    list_MAC = {}

    for i in arp_file.readlines():
        if line:
            list_MAC[i.split()[3]] = i.split()[0]
        line += 1

    arp_file.close()
    return(list_MAC)


def isConnected(ip): 

    """
    Returns True if a user is logged in. 
    To do this check we send an ICMP control packet by pinging the client.
    If the client is not connected, returns False.
    """

    response = pyping.ping(ip)
    return response.ret_code == 0
