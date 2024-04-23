from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import SQLModel, Field, create_engine, Session

DBNAME = "rooms"

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

# Create tables (if they do not already exist)
SQLModel.metadata.create_all(bind=engine)

# Function to create a new session
def get_session():
    with Session(engine) as session:
        yield session
