import requests, json
import websocket

import config


class ChatClient(websocket.WebSocketApp):
    def __init__(self, username, password, on_message, on_error=None, on_open=None, on_close=None):
        self.username = username

        # get chat jwt token to authenticate with chat
        auth_data = {"username": username, "password": password}
        response = requests.post(url=config.CHAT_AUTHENTICATION_URL, data=json.dumps(auth_data))

        if not response.ok:
            raise Exception("failed to login to chat", response.json())

        jwt_response = response.json()
        headers = {
            "Authorization": f"{jwt_response["token_type"]} {jwt_response["access_token"]}"
        }

        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        print(cookies)
        if not cookies and cookies["jwt"]:
            raise Exception("no cookies were sent from the server - something is wrong")
        formatted_cookie = f"jwt={cookies['jwt']}"
        print("hi")
        print("connecting to socket")

        super().__init__(url=config.CHAT_SOCKET_URL, on_message=on_message, on_error=self._error, on_open=on_open, on_close=on_close, header=headers, cookie=formatted_cookie)

    def send_chat_message(self, recipient: str, message: str) -> None:
        print("in send_chat_message")
        message_dict = {"recipient": recipient, "message": message}
        message_json = json.dumps(message_dict)
        self.send_text(message_json)

    @staticmethod
    def _error(ws, exc: Exception) -> None:
        print("got exception {}".format(exc))
        raise exc



