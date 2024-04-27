import requests, json, websocket

from drone import Drone
import config


class DroneCommandReceiver:

    def __init__(self, chat_username, chat_password, drone_ip, drone_port):
        #authenticate with the chat app
        data = {'username': chat_username, 'password': chat_password}
        response = requests.post(url=config.CHAT_AUTHENTICATION_URL, data=json.dumps(data))
        print(response.json())
        #open a socket with the chat
        #self.socket = websocket.WebsocketApp(config.CHAT_SOCKET_URL)
        #create a drone instance (using the drone class)
        self.drone = Drone(drone_ip, drone_port)


    def listen_to_commands(self):
        self.socket.connect(("localhost", 8000))
        self.socket.send("hi")

