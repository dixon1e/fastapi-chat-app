from sqlmodel import Session, select
import models
from database import RoomDB

def create_room(db: Session, room: models.Room):
    db_room = RoomDB(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: str):
    statement = select(RoomDB).where(RoomDB.id == room_id)
    result = db.exec(statement)
    return result.first()

def get_rooms(db: Session):
    statement = select(RoomDB)
    result = db.exec(statement)
    return result.fetchall()

