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
        response = self._send_command(command_id=mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=1)
        print(response)

    def takeoff(self, altitude, longitude=0, latitude=0, yaw=1):
        response = self._send_command(command_id=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, param4=yaw, param5=latitude, param6=longitude, param7=altitude)
        print(response)

    def change_altitude(self, altitude, delay=1):
        self.goto(altitude=altitude, delay=delay)

    def land(self, latitude=0, longitude=0, altitude=0, yaw=0):
        response = self._send_command(command_id=mavutil.mavlink.MAV_CMD_NAV_LAND, param4=yaw, param5=latitude, param6=longitude, param7=altitude)
        print(response)

    def goto(self, latitude=0, longitude=0, altitude=0, delay=1):
        response = self._send_command(command_id=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, param1=delay,param5=latitude, param6=longitude, param7=altitude)
        print(response)

    def get_location(self):
        response = self._req_message_get_response(message_type='GLOBAL_POSITION_INT', message_id=mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT)
        print(response)

    def get_speed(self):
        response = self._req_message_get_response(message_type='CONTROL_SYSTEM_STATE', message_id=mavutil.mavlink.MAVLINK_MSG_ID_CONTROL_SYSTEM_STATE)
        print(response)

    def get_battery(self):
        response = self.connection.recv_match(type='BATTERY_STATUS', blocking=True)
        print(response)

    def is_armed(self):
        self.connection.motors_armed()

    def _send_command(self, command_id, param1=0, param2=0, param3=0, param4=0, param5=0, param6=0, param7=0):
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
            param1,  # param1
            param2,  # param2
            param3,  # param3
            param4,  # param4
            param5,  # param5
            param6,  # param6
            param7  # param7
        )

        # Send the COMMAND_LONG
        self.connection.mav.send(message)

        response = self.connection.recv_match(type='COMMAND_ACK', blocking=True)

        return response

    def _request_message(self, message_id, req_param1=0, req_param2=0, req_param3=0, req_param4=0, req_param5=0, response_target=0):
        self._send_command(mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, param1=message_id, param2=req_param1, param3=req_param2, param4=req_param3, param5=req_param4, param6=req_param5, param7=response_target)

    def _req_message_get_response(self, message_type, message_id, req_param1=0, req_param2=0, req_param3=0, req_param4=0, req_param5=0, response_target=0):
        self._request_message(message_id, req_param1, req_param2, req_param3, req_param4, req_param5, response_target)
        response = self.connection.recv_match(type=message_type, blocking=True)
        return response

