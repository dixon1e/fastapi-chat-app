from sqlmodel import Session, select
import models
from database import RoomDB, MessageDB

def create_room(db: Session, room: str):
    db_room = RoomDB(name=room)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: str):
    statement = select(RoomDB).where(RoomDB.id == room_id)
    result = db.exec(statement)
    return result.first()

def get_room_by_name(db: Session, room_name: str):
    statement = select(RoomDB).where(RoomDB.name == room_name)
    result = db.exec(statement)
    return result.first()

# Returns list of JSON
def get_room_messages(db: Session, room_id: str):
    statement = select(MessageDB).where(MessageDB.room_id == room_id)
    result = db.exec(statement)
    messages = result.all()
    return messages

def get_rooms(db: Session):
    statement = select(RoomDB)
    result = db.exec(statement)
    return result.fetchall()

def delete_room(db: Session, room_id: str):
    statement = delete(RoomDB).where(RoomDB.name == room_id)
    result = db.exec(statement)
    return result

