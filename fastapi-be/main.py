from fastapi import FastAPI, WebSocket, Depends, HTTPException
from starlette.websockets import WebSocketDisconnect 
from sqlmodel import Session
from database import get_session, RoomDB, MessageDB
from models import Room, Message
from typing import Dict, List
from datetime import datetime, timezone
import pprint
import crud
import json

app = FastAPI()

active_connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/messages/{room_id}")
async def websocket_endpoint(room_id: str, websocket: WebSocket, db: Session = Depends(get_session)):
    room = crud.get_room_by_name(db, room_id)
    if not room:
        await websocket.close(code=1000)  # Normal closure
        return

    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    try:
        await websocket.accept()
        while True:
            now_utc = datetime.now(timezone.utc)
            message_json = await websocket.receive_text()
            message_dict = json.loads(message_json)
            message_data = {
                "room_id": room_id,
                "user_id": message_dict["user_id"],
                "message": message_dict["message"],
                "rcvd_at": now_utc.isoformat()
            }
            print("========================")
            pprint.pp(message_data)
            print("========================")
            # Broadcast to all except sender
            for connection in active_connections[room_id]:
                if connection != websocket:
                    await connection.send_text(json.dumps(message_data))
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
        if not active_connections[room_id]:
            del active_connections[room_id]
#     finally:
#         if websocket in active_connections[room_id]:
#             active_connections[room_id].remove(websocket)
#         if not active_connections[room_id]:
#             del active_connections[room_id]


@app.get("/rooms")
def get_rooms(db: Session = Depends(get_session)):
    rooms = crud.get_rooms(db)
    return {"rooms": rooms}

@app.get("/rooms/{room_id}")
def get_room(room_id: str, db: Session = Depends(get_session)):
    room = crud.get_room(db, room_id)
    if room:
        return {"id": room.id, "name": room.name}
    raise HTTPException(status_code=404, detail="Room not found")

@app.get("/rooms/search/{room_name}")
def get_room_by_name(room_name: str, db: Session = Depends(get_session)):
    room = crud.get_room_by_name(db, room_name)
    if room:
        return {"id": room.id, "name": room.name}
    raise HTTPException(status_code=404, detail="Room not found")

@app.get("/rooms/{room_id}/messages")
def get_room(room_id: str, db: Session = Depends(get_session)):
    messages = crud.get_room_messages(db, room_id)
    if messages:
        return {"room_id": room.id, "messages": messages}
    raise HTTPException(status_code=404, detail="Room not found")

@app.post('/rooms')
def create_room(room: Room, db: Session = Depends(get_session)):
    print(f"Create Rooms Received: {room}")
    db_room = crud.create_room(db, room.name)
    return {"room": db_room.name}

@app.delete("/rooms/{room_id}")
def delete_room(room_id: str, db: Session = Depends(get_session)):
    rooms = crud.delete_room(db, room_id)
    return rooms

