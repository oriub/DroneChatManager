import json
import os
import threading

from drone import Drone
from chatclient import ChatClient


class DroneCommandReceiver:
    def __init__(self, chat_username, chat_password, drone_ip, drone_port):
        self.chat_client = ChatClient(username=chat_username, password=chat_password, on_message=self._handle_message)
        self.drone = Drone(drone_ip, drone_port)
        threading.Thread(self.chat_client.run_forever())

    def _handle_message(self, websocket, message):
        """
        when a message is sent in chat, check if its one of the drone's supported commands
        if it is run it, otherwise send a help message
        :param websocket: websocket object
            websocket object, it is not used but necessary for this function to be sent to the WebSocketApp object
        :param message: str
            message that was sent in the chat
        :return:
            void
        """
        print("recived message: " + message)
        # generate possible commands list and help message
        commands = self._generate_drone_commands()
        help_text = self._generate_commands_help_message()

        msg_dict = json.loads(message)
        other_user = msg_dict["sender"]
        # split command and arguments into a list
        split_message = msg_dict["message"].split(" ")
        command = split_message[0].lower()

        # if the message sent was a valid command
        if command in commands.keys():
            print(f"command {command} is valid!")
            command_func = commands[command][0]
            try:
                # get arguments sent in message
                args = [float(a) for a in split_message[1:]]
                # if there were arguments in the message
                if len(args) == 0:
                    resp = command_func(self.drone)
                else:
                    resp = command_func(self.drone, *args)
                self.chat_client.send_chat_message(recipient=other_user, message="command sent successfully!")
                self.chat_client.send_chat_message(recipient=other_user, message=str(resp))

            except Exception as e:
                self.chat_client.send_chat_message(recipient=other_user,
                                                   message=f" error while running command {command}: {e}")

        else:
            self.chat_client.send_chat_message("invalid command, please use one of the following commands")
            self.chat_client.send_chat_message(recipient=other_user, message=help_text)

    @staticmethod
    def _generate_drone_commands():
        """
        Generates a dict containg all the command names, arguments and function objects of the drone object
        :return:
        dict that looks like this
        {method name: [method function object, argument names]}
        """
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
        '''
        Generates a help string containg a list of commands that can be sent to the drone,
        along with the arguments that can or should be sent
        :return:
        str containing all methods of the drone (not including builtins or protected ones), and parmeters
        '''
        commands_dict = DroneCommandReceiver._generate_drone_commands()
        # create a list of every command's name and parameters
        commands_help = [f"{c} <{commands_dict[c][1]}> \n || " for c in commands_dict.keys()]
        # return the list as one string
        return "\n".join(commands_help)
