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
        print("recived message: " + message)
        commands = self._generate_drone_commands()
        help_text = self._generate_commands_help_message()

        msg_dict = json.loads(message)
        other_user = msg_dict["sender"]
        split_message = msg_dict["message"].split(" ")
        command = split_message[0].lower()
        args = [float(a) for a in split_message[1:]]
        print(f"args {args}")
        try:
            if command in commands.keys():
                print(f"command {command} is valid!")

                command_func = commands[command][0]
                try:
                    if len(args) == 0:
                        resp = command_func(self.drone)
                    else:
                        resp = command_func(self.drone, *args)
                    self.chat_client.send_chat_message(recipient=other_user, message=str(resp))

                except Exception as e:
                    self.chat_client.send_chat_message(recipient=other_user,
                                                       message=f" error {e} while running command {command}")

            else:
                self.chat_client.send_chat_message(recipient=other_user, message=help_text)

        except Exception as e:
            print("caught exception!", e)

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
        commands_help = [f"{c} {commands_dict[c][1]} \n || " for c in commands_dict.keys()]
        return "\n".join(commands_help)
