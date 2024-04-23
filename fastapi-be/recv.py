import json
import asyncio
import requests
import websockets

async def receive_messages(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print("Received:", message)

if __name__ == "__main__":
# Get a list of the rooms
    r = requests.get("http://localhost:8000/rooms")
    rooms  = json.loads(r.text)
    rooms  = rooms["rooms"]

# Pick a random room for now
    roomid = str(rooms[0]["id"])

# Receive a Chat Message from this Room
    uri = f"ws://localhost:8000/messages/{roomid}"
    print(f"Listening to: {uri}")
    while True:
        asyncio.run(receive_messages(uri))

