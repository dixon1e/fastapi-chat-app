from sqlmodel import SQLModel, Field

class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    room_id: int
    user_id: str
    message: str
    rcvd_at: str

