import sys
import json
import asyncio
import requests
import websockets

async def receive_messages(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print("Received:", message)
            print("=========")

if __name__ == "__main__":

    headers = {"accept": "application/json", "Content-Type": "application/json" }

# Get a list of the rooms
    r = requests.get("http://localhost:8000/rooms", headers=headers)
    rooms  = json.loads(r.text)
    room_names  = [ item["name"] for item in rooms["rooms"] ]

# Show to user for selection information
    print("Existing rooms:")
    for item in room_names:
        print(item)
    room = input("Enter room (type 'exit' to quit): ")
    if room.lower() == 'exit':
        sys.exit()

# We have a room name that either exists or not
    url = f"http://localhost:8000/rooms/search/{room}"
    r = requests.get(url)
# If not exist loop around until exists
    while r.status_code != 200:
        print(f"Could not find room: {room}")
        room = input("Enter room (type 'exit' to quit): ")
        if room.lower() == 'exit':
            sys.exit()
        url = f"http://localhost:8000/rooms/search/{room}"
        r = requests.get(url)

    print(f"Selected: {room}")

# Pick a random room for now
#    room = str(rooms[0]["id"])

# Receive a Chat Message from this Room
    uri = f"ws://localhost:8000/messages/{room}"
    print(f"Listening to: {uri}")
    while True:
        asyncio.run(receive_messages(uri))

