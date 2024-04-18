import sys
import json
import requests
import asyncio
import websockets
from uuid import uuid4


async def send_message(uri, message):
    # Customize ping interval and timeout
    # ping_interval = 10  # seconds
    # ping_timeout  = 10  # seconds

    async with websockets.connect(
        uri,
      #   ping_interval=ping_interval,
      #   ping_timeout=ping_timeout
    ) as websocket:
        await websocket.send(message)

if __name__ == "__main__":

    headers = {"accept": "application/json", "Content-Type": "application/json" }


# Create a new conversation room
#     room_name = str(uuid4())
#     data = {"name" : room_name}
#     json_data = json.dumps(data)
#     r = requests.post("http://localhost:8000/rooms", headers=headers, data=json_data)
#     print(f"RoomID: {r.json()}")

# Get a list of the rooms
    r = requests.get("http://localhost:8000/rooms")
    rooms  = json.loads(r.text)
    rooms  = rooms["rooms"]

# Pick a random room for now
    roomid = str(rooms[0]["name"])

# Send a Chat Message to this Room
    uri = f"ws://localhost:8000/messages/{roomid}"
    print(uri)
    while True:
        message = input("Enter message (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        asyncio.run(send_message(uri, message))

