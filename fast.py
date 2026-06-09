from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import engine
import models
from schemas import ClientCreate, ClientResponse, ClientUpdate

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Привет"}

@app.post("/clients", response_model=ClientResponse)
def create_client(client: ClientCreate):
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

        