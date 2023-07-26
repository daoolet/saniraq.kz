from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session


from .database import SessionLocal, Base, engine

from .actions import UsersRepository
from .schemas import UserCreate


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
def post_signup(
    name: str,
    email: str,
    password: str,
    city: str,
    phone: str,
    db: Session = Depends(get_db)
):
    
    user_exists = users_repository.get_by_email(db, user_email=email)

    if user_exists:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    new_user = UserCreate(email=email, name=name, password=password, city=city, phone=phone)
    answer = users_repository.save_user(db, user=new_user)

    return answer