from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    phone: str
    budget: int

class ClientResponse(BaseModel):
    id: int
    name: str
    phone: str
    budget: int

class ClientUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None 
    budget: int | None = None