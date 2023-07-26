from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session


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
    
    user_exists = users_repository.get_by_email(db, user_email=user.email)

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