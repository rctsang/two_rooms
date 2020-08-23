from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class Player(Base):
    __tablename__ = 'Players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    gameroom = db.Column(db.String(4), index=True)
    room = db.Column(db.Integer)
    role = db.Column(db.String(15), index=True)

    def __init__(self, name, gameroom=None, room=None, role=None):
        self.name = name
        self.gameroom = gameroom
        self.room = room
        self.role = role


# Create tables.
Base.metadata.create_all(bind=engine)
