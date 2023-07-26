from fastapi import FastAPI, HTTPException, Depends, Response, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose import jwt

from .database import SessionLocal, Base, engine
from .actions import UsersRepository
from .schemas import UserCreate, UserInput


app = FastAPI()
Base.metadata.create_all(bind=engine)


users_repository = UsersRepository()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return Response("Welcome to Saniraq.kz", status_code=200)


# ------------ SIGN UP ------------

@app.get("/auth/users")
def get_signup(db: Session = Depends(get_db)):
    all_users = users_repository.get_all(db)
    return all_users

@app.post("/auth/users")
def post_signup(user: UserInput, db: Session = Depends(get_db)):
    
    user_exists = users_repository.get_by_phone(db, user_phone=user.phone)

    if user_exists:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    new_user = UserCreate(
        email = user.email,
        name = user.name,
        password = user.password,
        city = user.city,
        phone = user.phone
    )

    users_repository.save_user(db, user=new_user)
    return Response("User is registred", status_code=200)


# ------------ LOGIN ------------

def create_jwt_token(phone: str) -> str:
    body = {"phone": phone}
    token = jwt.encode(body, "kek", "HS256")
    return token

def decode_jwt_token(token: str) -> int:
    data = jwt.decode(token, "kek", "HS256")
    return data["phone"]

@app.post("/auth/users/login")
def post_login(
    phone: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_exists = users_repository.get_by_phone(db, phone)

    if not user_exists:
        return Response("User does not exists with this phone number")
    
    if user_exists.password != password:
        return Response("Passwords dont match")
    
    token = create_jwt_token(user_exists.phone)
    return JSONResponse(content={"access_token": token}, status_code=200)