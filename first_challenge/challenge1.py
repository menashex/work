import json
from netmiko import ConnectHandler
from getpass import getpass
import os
import sys
164325897Aa
file_path = sys.path[0]
os.environ['NET_TEXTFSM'] = file_path + "\\ntc_templates\\templates"

ipadd = input("please enter device ip address: ")
portnum = input("please enter port number (default - 22): ")
if(len(portnum) ==  0):
    portnum = 22
devicetype = input("please enter device type: ")
username = input("please enter remote access username: ")
password = getpass(prompt="please enter remote access password: ")

device={
        "device_type": devicetype,
        "host": ipadd,
        "port": portnum, 
        "username": username,
        "password": password,
}


try:
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    data = net_connect.send_command("show ip int brief | inc up", use_textfsm=True)
    print(json.dumps(data, indent=2))
    with open(file_path + "\\results.txt","w") as file:
        json.dump(data, file, indent=6)

except Exception as e:
    print(e)
    with open(file_path + "\\errors.txt","w") as file:
        file.write(str(e))

while(1):
    i=1