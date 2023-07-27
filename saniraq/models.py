from sqlalchemy import Column, Float, Integer, String

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    city = Column(String)
    phone = Column(String)

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String) 
    price = Column(Float)  
    adress = Column(String) 
    area = Column(Float)  
    rooms_count = Column(Float) 
    description = Column(String) 