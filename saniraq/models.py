from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    city = Column(String)
    phone = Column(String)

    ad = relationship("Ad", back_populates="ad_owner")

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String) 
    price = Column(Float)  
    adress = Column(String) 
    area = Column(Float)  
    rooms_count = Column(Integer) 
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    ad_owner = relationship("User", back_populates="ad")