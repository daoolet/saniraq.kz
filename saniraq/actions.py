# user repo with methods and etc
from sqlalchemy.orm import relationship, Session

from .models import User
from .schemas import UserCreate


class UsersRepository:

    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()
    
    def get_by_email(self, db: Session, user_email: str):
        return db.query(User).filter(User.email == user_email).first()
    
    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def save_user(self, db: Session, user: UserCreate):
        db_user = User(email=user.email, name=user.name, password=user.password, city=user.city, phone=user.phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
