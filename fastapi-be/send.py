import sys
import json
import requests
import asyncio
import websockets
from uuid import uuid4

user_id = str(uuid4())

def select_from_list(rooms):
    """Provides a way to select a room from a list using keyboard-like input."""

    for i, room in enumerate(rooms):
        print(f"{i+1}. {room}")

    while True:
        try:
            choice = int(input("Enter the number of your desired room: "))
            if 0 < choice <= len(rooms):
                return rooms[choice - 1]  # Subtract 1 for zero-based indexing
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


async def send_message(uri, message):
    # Customize ping interval and timeout for connection setup only
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


# Get a list of the rooms
    r = requests.get("http://localhost:8000/rooms", headers=headers)
    rooms  = json.loads(r.text)
    room_names  = [ item["name"] for item in rooms["rooms"] ]

# Show to user for selection information
    print("Choose from an existing room or enter new room to be created:")
    for item in room_names:
        print(item)
    room = input("Enter room (type 'exit' to quit): ")
    if room.lower() == 'exit' or room.lower() == 'quit':
        sys.exit()

# We have a room name that either exists or not
    url = f"http://localhost:8000/rooms/search/{room}"
    r = requests.get(url)
# If not exist we create a new room
    if r.status_code != 200:
        data = {"name":room}
        r = requests.post("http://localhost:8000/rooms", json=data, headers=headers)
        if r.status_code == 422:
            error_data = r.json() 
            # Adapt the following line based on your actual error structure
            error_message = error_data["detail"][0]["msg"] 
            print(f"Room creation failed: {error_message}") 
            sys.exit()
        result = json.loads(r.text)
        room = result["room"]

# Chat Messages with this Room
    uri = f"ws://localhost:8000/messages/{room}"
    while True:
        message = input("Enter message (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        message_json = {"user_id":user_id, "message":message}
        message_text = json.dumps(message_json)
        asyncio.run(send_message(uri, message_text))

