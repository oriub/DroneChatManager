import requests, json
import websocket

import config


class ChatClient:
    def __init__(self, username, password, on_message_function):
        # get chat jwt token to authenticate with chat
        auth_data = {"username": username, "password": password}
        response = requests.post(url=config.CHAT_AUTHENTICATION_URL, data=json.dumps(auth_data))
        jwt_response = response.json()
        
        headers = {
            "Authorization": f"{jwt_response["token_type"]} {jwt_response["access_token"]}"
        }

        self.socket = websocket.WebSocketApp(config.CHAT_SOCKET_URL, on_message=on_message_function, header=headers)


async def msg(ws, m):
    print(m)


cl = ChatClient("1", "1", msg)
cl.socket.run_forever()

