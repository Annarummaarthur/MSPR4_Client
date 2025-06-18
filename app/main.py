from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from app.db import SessionLocal, Base, engine
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN")


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=403, detail="Accès interdit")


app = FastAPI(title="API Gestion des Clients")


class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    username = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    profile_first_name = Column(String, nullable=True)
    profile_last_name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


class Client(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    profile_first_name: Optional[str] = None
    profile_last_name: Optional[str] = None
    company_name: Optional[str] = None


class ClientUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    profile_first_name: Optional[str] = None
    profile_last_name: Optional[str] = None
    company_name: Optional[str] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/clients", response_model=Client)
def create_client(
    client: Client,
    db: Session = Depends(get_db),
        _: HTTPAuthorizationCredentials = Security(verify_token),
):
    db_client = ClientModel(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.get("/clients", response_model=List[Client])
def list_clients(
    db: Session = Depends(get_db),
        _: HTTPAuthorizationCredentials = Security(verify_token),
):
    return db.query(ClientModel).all()


@app.get("/clients/{client_id}", response_model=Client)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
        _: HTTPAuthorizationCredentials = Security(verify_token),
):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client


@app.put("/clients/{client_id}", response_model=Client)
def update_client(
    client_id: int,
    updated_client: ClientUpdate,
    db: Session = Depends(get_db),
        _: HTTPAuthorizationCredentials = Security(verify_token),
):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    for field, value in updated_client.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", response_model=dict)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
        _: HTTPAuthorizationCredentials = Security(verify_token),
):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    db.delete(client)
    db.commit()
    return {"message": "Client supprimé avec succès"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
