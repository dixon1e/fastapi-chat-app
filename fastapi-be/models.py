from sqlmodel import SQLModel

class Room(SQLModel):
    name: str
