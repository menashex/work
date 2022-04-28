from distutils.cmd import Command
import json
from multiprocessing.sharedctypes import Value
from netmiko import ConnectHandler
import sys
from getpass import getpass
import os

file_path = sys.path[0]
os.environ['NET_TEXTFSM'] = file_path + "\\ntc_templates\\templates"
actionfile = file_path + "\\config.txt"
changesfile = file_path + "\\changes.txt"

ipadd = input("please enter device ip address: ")
portnum = input("please enter port number (default - 22): ")
if(len(portnum) ==  0):
    portnum = 22
devicetype = input("please enter device type: ")
username = input("please enter remote access username: ")
password = getpass(prompt="please enter remote access password: ")

#device={
#        "device_type": devicetype,
#        "host": ipadd,
#        "port": portnum, 
#        "username": username,
#        "password": password,
#        "actionfile": file_path + "\\config.txt",
#}
device={
        "device_type": "cisco_ios",
        "host": "10.0.0.13",
        "port": "22", 
        "username": "menash",
        "password": "menash",
}

net_connect = ConnectHandler(**device)
net_connect.enable()
data = net_connect.send_command("show ip int brief", use_textfsm=True)
dict=[]
with open(actionfile) as file:
    for current_line in file:
        (interface, status, ipaddr) = current_line.split(" ")
        dict.append({"intf":interface, "status":status.lower(), "ipaddr":ipaddr.replace("\n","")})

for i in data:
    for k in dict:
        if(k["intf"] == i["intf"]):
            print("\n", k["intf"], ":", sep="")
            if(k["status"] != i["status"]):
                print(i["status"] + " --->", k["status"])
            if(k["ipaddr"] != i["ipaddr"]):
                print(i["ipaddr"] + " ---> ", k["ipaddr"])                


#except Exception as e:
 #   print(e)
  #  with open(file_path + "\\errors.txt","w") as file:
   #     file.write(str(e))