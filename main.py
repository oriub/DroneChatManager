from commandreceiver import DroneCommandReceiver
import config

manager = DroneCommandReceiver(config.CHAT_USERNAME, config.CHAT_PASSWORD, config.DRONE_IP, config.DRONE_PORT)
