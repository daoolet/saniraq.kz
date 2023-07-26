from pydantic import BaseModel

class UserInput(BaseModel):
    email: str
    password: str
    name: str
    city: str
    phone: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    city: str
    phone: str