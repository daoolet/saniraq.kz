from sqlalchemy.orm import relationship, Session

from .models import User, Ad
from .schemas import (
    UserCreate,
    UserUpdate,
    AdCreate
)


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
    

class AdsRepository:

    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Ad).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, ad_id: int):
        return db.query(Ad).filter(Ad.id == ad_id).first()

    def save_ad(self, db: Session, ad: AdCreate, user_id: int):
        db_ad = Ad(
            type = ad.type,
            price = ad.price,
            adress = ad.adress,
            area = ad.area,
            rooms_count = ad.rooms_count,
            description = ad.description,
            user_id = user_id
        )
        db.add(db_ad)
        db.commit()
        db.refresh(db_ad)
        return db_ad
    
    def update_ad(self, db: Session, ad_id: int, new_info: AdCreate):
        db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
        db_ad.type = new_info.type
        db_ad.price = new_info.price
        db_ad.adress = new_info.adress
        db_ad.area = new_info.area
        db_ad.rooms_count = new_info.rooms_count
        db_ad.description = new_info.description
        db.commit()
        return True
    
    def delete_ad(self, db: Session, ad_id: int):
        db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
        db.delete(db_ad)
        db.commit()
        return True
