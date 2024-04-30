from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session

from typing import List, Optional

DBNAME = "conversations"

def create_database_if_not_exists(url):
    if not database_exists(url):
        create_database(url)
    print("Database exists or was created!")

# Define the database URL
POSTGRES_DATABASE_URL = f"postgresql://postgres:postgres@db/{DBNAME}"

# Check and create database if necessary
create_database_if_not_exists(POSTGRES_DATABASE_URL)

# Create the engine
engine = create_engine(POSTGRES_DATABASE_URL)

# Define the RoomDB model using SQLModel
class RoomDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    messages: List["MessageDB"] = Relationship(back_populates="room")

# Define the MessageDB model using SQLModel
class MessageDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    room_id: int = Field(default=None, foreign_key="roomdb.id")
    room: Optional["RoomDB"] = Relationship(back_populates="messages")

# Create tables (if they do not already exist)
SQLModel.metadata.create_all(bind=engine)

# Function to create a new session
def get_session():
    with Session(engine) as session:
        yield session
