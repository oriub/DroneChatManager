from pymavlink import mavutil


class Drone:
    def __init__(self, ip_address, port, protocol="udpin"):
        connection_str = f"{protocol}:{ip_address}:{port}"

        print(f"connecting with {connection_str}")
        self.connection = mavutil.mavlink_connection(connection_str)
        print(f"waiting for heartbeat...")
        self.connection.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.connection.target_system,
                                                                  self.connection.target_component))

    def arm(self):
        response = self._send_message(command_id=mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=1)
        print(response)

    def takeoff(self):
        response = self._send_message(command_id=mavutil.mavlink.MAV_CMD_)

    def change_altitude(self):
        pass

    def land(self):
        pass

    def get_location(self):
        pass

    def get_speed(self):
        pass

    def get_battery(self):
        response = self.connection.recv_match(type='BATTERY_STATUS', blocking=True)
        print(response)

    def is_armed(self):
        pass

    def _send_message(self, command_id, param1=0, param2=0, param3=0, param4=0, param5=0, param6=0, param7=0):
        '''
        Send a command to the drone as a COMMAND_LONG
        :param command_id:
        :param param1:
        :param param2:
        :param param3:
        :param param4:
        :param param5:
        :param param6:
        :param param7:
        :return:
        '''
        message = self.connection.mav.command_long_encode(
            self.connection.target_system,  # Target system ID
            self.connection.target_component,  # Target component ID
            command_id,  # ID of command to send
            0,  # Confirmation
            param1,  # param1: Message ID to be streamed
            param2,  # param2: Interval in microseconds
            param3,  # param3 (unused)
            param4,  # param4 (unused)
            param5,  # param5 (unused)
            param6,  # param6 (unused)
            param7  # param7 (unused)
        )

        # Send the COMMAND_LONG
        self.connection.mav.send(message)

        response = self.connection.recv_match(type='COMMAND_ACK', blocking=True)

        return response

