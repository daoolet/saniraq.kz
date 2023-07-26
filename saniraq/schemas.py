
from pydantic import BaseModel
from attr import define


@define
class UserCreate:
    email: str
    password: str
    name: str
    city: str
    phone: str