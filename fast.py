from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine
import models
from schemas import ClientCreate, ClientResponse, ClientUpdate, UserCreate, Token
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Привет"}

@app.post("/clients", response_model=ClientResponse)
def create_client(client: ClientCreate, current_user: str = Depends(get_current_user)):
    with Session(engine) as session:
        new_client = models.Client(
            name=client.name, 
            phone=client.phone, 
            budget=client.budget
        )
        session.add(new_client)
        session.commit()
        session.refresh(new_client)
        return new_client

@app.get("/clients", response_model=list[ClientResponse])
def get_clients():
    with Session(engine) as session:
        clients = session.query(models.Client).all()
        return clients

@app.get("/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: int):
    with Session(engine) as session:
        client = session.get(models.Client, client_id)
        if client is None:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        return client

@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    with Session(engine) as session:
        client = session.get(models.Client, client_id)
        if client is None:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        removed_name = client.name
        session.delete(client)
        session.commit()
        return {"message": f"Клиент {removed_name} удален!"}

@app.put("/clients/{client_id}")
def update_client(client_id: int, client_data: ClientUpdate):
    with Session(engine) as session:
        client = session.get(models.Client, client_id)
        if client is None:
            raise HTTPException(status_code = 404, detail="Клиент не найден")
        if client_data.name is not None:
            client.name = client_data.name
        if client_data.phone is not None:
            client.phone = client_data.phone
        if client_data.budget is not None:
            client.budget = client_data.budget
        session.commit()
        session.refresh(client)
        return client

@app.post("/register")
def register(user_data: UserCreate):
    with Session(engine) as session:
        existing_user = session.query(models.User).filter_by(username=user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь уже существует!")
        new_user = models.User(
            username=user_data.username,
            hashed_password=hash_password(user_data.password)    
        )
        session.add(new_user)
        session.commit()
        return {"message": f"Пользователь {user_data.username} зарегистрирован!"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.query(models.User).filter_by(username=form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}