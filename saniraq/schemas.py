from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    password: str
    name: str
    city: str
    phone: str

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    city: str
    phone: str

class UserUpdate(BaseModel):
    name: str
    city: str
    phone: str

class AdCreate(BaseModel):
    type: str
    price: float
    adress: str
    area: float
    rooms_count: float
    description: str