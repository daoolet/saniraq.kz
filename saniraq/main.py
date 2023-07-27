from fastapi import FastAPI, HTTPException, Depends, Response, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from .database import SessionLocal, Base, engine
from .actions import UsersRepository, AdsRepository
from .schemas import (
    UserCreate,
    UserInput,
    UserUpdate,
    AdCreate
)


app = FastAPI()
Base.metadata.create_all(bind=engine)


users_repository = UsersRepository()
ads_repository = AdsRepository()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return Response("Welcome to Saniraq.kz", status_code=200)


# ------------ TASK1 - SIGN UP ------------

@app.get("/auth/users")
def get_signup(db: Session = Depends(get_db)):
    all_users = users_repository.get_all(db)
    return all_users

@app.post("/auth/users")
def post_signup(user: UserInput, db: Session = Depends(get_db)):
    
    user_exists = users_repository.get_by_username(db, user.username)

    if user_exists:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    new_user = UserCreate(
        username = user.username,
        name = user.name,
        password = user.password,
        city = user.city,
        phone = user.phone
    )

    users_repository.save_user(db, user=new_user)
    return Response("User is registred", status_code=200)


# ------------ TASK2 - LOGIN ------------

def create_jwt_token(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "kek", "HS256")
    return token

@app.post("/auth/users/login")
def post_login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_exists = users_repository.get_by_username(db, username)

    if not user_exists:
        return HTTPException(status_code=404, detail="User does not exists with this phone number")
    
    if user_exists.password != password:
        return Response("Passwords dont match")
    
    token = create_jwt_token(user_exists.id)
    return {"access_token": token}


# ------------ TASK3 - UPDATE ------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/users/login")

def decode_jwt_token(token: str) -> int:
    data = jwt.decode(token, "kek", "HS256")
    return data["user_id"]

@app.patch("/auth/users/me")
def patch_update_user(
    phone: str,
    name: str,
    city: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    current_user_id = decode_jwt_token(token)
    
    new_info = UserUpdate(
        name = name,
        phone = phone,
        city = city
    )

    updated_user = users_repository.update_user(db, user_id=current_user_id, new_info=new_info)
    
    if not updated_user:
        raise HTTPException(status_code = 400, detail="Update did not happen")
    
    return Response("Updated - OK", status_code = 200)


# ------------ TASK4 - GET ------

@app.get("/auth/users/me")
def get_user_info(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    current_user_id = decode_jwt_token(token)
    current_user_info = users_repository.get_by_id(db, user_id=current_user_id)

    return current_user_info


# ------------ TASK5 - POST AD ------

@app.post("/shanyraks")
def post_ad(
    input_ad: AdCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    current_user_id = decode_jwt_token(token)
    saved_ad = ads_repository.save_ad(db, input_ad)
    #   new_ad = AdCreate(
    #       type = input_ad.type,
    #       price = input_ad.price,
    #       adress = input_ad.adress,
    #       area = input_ad.area,
    #       rooms_count = input_ad.rooms_count,
    #       description = input_ad.description
    # )
    return {"ad_id": saved_ad.id}

# ------------ TASK6 - GET AD ------

@app.get("/shanyraks/{id}")
def get_ad(id: int, db: Session = Depends(get_db)):
    
    found_ad = ads_repository.get_by_id(db, ad_id=id)

    if not found_ad:
        raise HTTPException(status_code=404, detail="Not found ad")
    
    return found_ad



    