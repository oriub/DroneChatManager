import time

from drone import Drone
from commandreceiver import DroneCommandReceiver


ip = "172.19.16.1"
port = 14550


'''
TODO:
1. make values returned by drone be good
2. throw errors from drone if command failed
3. create chat client
4. map drone method to command in commandreciever
5. 
'''

manager = DroneCommandReceiver("1", "1", ip, port,)
manager.drone.arm()