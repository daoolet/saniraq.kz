from pydantic import BaseModel


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
    rooms_count: int
    description: str