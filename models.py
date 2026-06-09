from database import Base, engine
from sqlalchemy import Column, Integer, String

class Client(Base):
    __tablename__ = "clients"
    id     = Column(Integer, primary_key=True)
    name   = Column(String(50), nullable=False)
    phone  = Column(String(20), nullable=False, unique=True)
    budget = Column(Integer, nullable=False)

Base.metadata.create_all(engine)