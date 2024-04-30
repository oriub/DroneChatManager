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


drone = Drone(ip_address=ip, port=port)
drone.arm()
time.sleep(5)
drone.takeoff(10)
drone.get_location()
#drone.goto(-35.363240,149.2,20)
#drone.get_speed()
drone.is_armed()
drone.get_battery()
drone.change_altitude(15)
drone.get_location()
drone.get_speed()
drone.land()

drone.get_speed()
#manager = DroneCommandReceiver("1", "1", ip, port,)
