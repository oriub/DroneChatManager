# DroneChatManager
DroneChatManger (DCM if you like) is a Python program that controls and gets telemetry from a drone (that runs arducopter) using a chat website.
It uses pymavlink to communicate with the drone, and a websocket to connect to the chat as a client. then users connected to the chat can send commands and get telemetry from the drone.

The chat is in a [different git repository](https://github.com/oriub/Chat), and should be set up and running before setting up and using this one.

## Setting Up and Running

**please make sure you have set up the [chat](https://github.com/oriub/Chat) prior to doing these steps**

1. start by cloning this repository
```
git clone https://github.com/oriub/DroneChatManager.git
```

2. then you should use the chat website and create a user that will be used to connect your drone to the chat (do not login after signing up).
![dronesignup](https://github.com/oriub/DroneChatManager/assets/164090680/8437e230-ea2d-459f-b126-1fb875b684d2)

3. continue by openning the config.py file, and filling in the information: 
![config](https://github.com/oriub/DroneChatManager/assets/164090680/ba4f97e1-ffb0-4755-9442-056becd3d373)

**CHAT_USERNAME**  the username you created for the drone to login with  
**CHAT_PASSWORD**  the password for that user  
**CHAT_ADDRESS**   address where the chat **backend** is running (probably "localhost:5000")  
**DRONE_IP**       IP address to contact the drone with  
**DRONE_PORT**     port where the drone is listening to connections  

Other options should not be touched.  

  
Then you can simply run main.py, and your drone should be connected to the chat and ready to receive commands!



