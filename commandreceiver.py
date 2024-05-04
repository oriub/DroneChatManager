import json
import os
import threading

from drone import Drone
from chatclient import ChatClient



class DroneCommandReceiver:
    def __init__(self, chat_username, chat_password, drone_ip, drone_port):
        self.chat_client = ChatClient(username=chat_username, password=chat_password, on_message=self._handle_message)

        print("Drone")
        self.drone = Drone(drone_ip, drone_port)
        threading.Thread(target=self.chat_client.run_forever())

    def _handle_message(self, websocket, message):
        # commands = self._generate_drone_commands()
        split_message = message.split(" ")
        #print(DroneCommandReceiver._generate_commands_help_message())
        print("hiiiii")
        os.mkdir("c:/test/")
        msg_dict = json.loads(message)
        print(msg_dict)
        self.drone.get_location()
        #self.chat_client.send_chat_message(recipient=msg_dict["sender"], message=msg_dict["message"])
        #self.chat_client.send_text("hi")
        # if message[0].lower() in commands.keys():
        #     print("command exists!")
        #     self.drone.commands[]



    @staticmethod
    def _generate_drone_commands():
        commands_dict = {}
        for attribute in dir(Drone):
            attr_object = getattr(Drone, attribute)
            if not attribute[0] == "_" and callable(attr_object):
                # get all function parameters (not including self)
                params = attr_object.__code__.co_varnames[1:attr_object.__code__.co_argcount]
                param_string = " ".join(params)
                commands_dict[attribute] = [getattr(Drone, attribute), param_string]

        return commands_dict
    @staticmethod
    def _generate_commands_help_message():
        commands_dict = DroneCommandReceiver._generate_drone_commands()
        # list of every command's name and parameters
        commands_help = [f"{commands_dict[c][0]} {commands_dict[c][1]}" for c in commands_dict.keys()]
        return "\n".join(commands_help)






