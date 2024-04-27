from drone import Drone
from commandreceiver import DroneCommandReceiver


ip = "172.19.16.1"
port = 14550


# drone = Drone(ip_address=ip, port=port)
# drone.arm()
# drone.get_battery()
manager = DroneCommandReceiver("1", "1", ip, port,)
