import time

from drone import Drone
from commandreceiver import DroneCommandReceiver


ip = "172.19.16.1"
port = 14550


drone = Drone(ip_address=ip, port=port)
#drone.arm()
#time.sleep(5)
drone.get_speed()
#manager = DroneCommandReceiver("1", "1", ip, port,)
