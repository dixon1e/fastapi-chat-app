from fastapi import FastAPI, WebSocket, Depends, HTTPException
from sqlmodel import Session
from database import get_session, RoomDB
from models import Room  # Ensure models.Room is properly defined to match RoomDB fields
from typing import Dict, List
import crud

app = FastAPI()

active_connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/messages/{room_id}")
async def websocket_endpoint(room_id: str, websocket: WebSocket, db: Session = Depends(get_session)):
    room = crud.get_room(db, room_id)
    if not room:
        await websocket.close(code=1000)  # Normal closure
        return

    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    try:
        await websocket.accept()
        while True:
            message = await websocket.receive_text()
            message_data = {
                "room_id": room_id,
                "message": message,
            }
            json_message = json.dumps(message_data)
            print("========================")
            # Broadcast to all except sender
            for connection in active_connections[room_id]:
                if connection != websocket:
                    await connection.send_text(json_message)
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
        if not active_connections[room_id]:
            del active_connections[room_id]
    finally:
        if websocket in active_connections[room_id]:
            active_connections[room_id].remove(websocket)
        if not active_connections[room_id]:
            del active_connections[room_id]


@app.post('/rooms')
def create_room_handler(room: Room, db: Session = Depends(get_session)):
    db_room = crud.create_room(db, room)
    return {"message": f"Room Id: {db_room.name} is created"}

@app.get("/rooms/{room_id}")
def get_room_handler(room_id: str, db: Session = Depends(get_session)):
    room = crud.get_room(db, room_id)
    if room:
        return {"id": room.id, "name": room.name}
    raise HTTPException(status_code=404, detail="Room not found")

@app.get("/rooms")
def get_rooms(db: Session = Depends(get_session)):
    rooms = crud.get_rooms(db)
    return {"rooms": rooms}

