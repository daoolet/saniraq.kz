# user repo with methods and etc
from sqlalchemy.orm import relationship, Session

from .models import User
from .schemas import UserCreate, UserUpdate


class UsersRepository:

    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()
    
    def get_by_username(self, db: Session, user_username: str):
        return db.query(User).filter(User.username == user_username).first()
    
    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def save_user(self, db: Session, user: UserCreate):
        db_user = User(username=user.username, name=user.name, password=user.password, city=user.city, phone=user.phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(self, db: Session, user_id: int, new_info: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.name = new_info.name
        # db_user.username = new_info.username
        # db_user.password = new_info.password
        db_user.city = new_info.city
        db_user.phone = new_info.phone
        db.commit()
        return True
