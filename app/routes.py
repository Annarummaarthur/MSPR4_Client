import os
from typing import List
from fastapi import HTTPException, Depends, Security, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import Client, ClientUpdate
from app.models import ClientModel

API_TOKEN = os.getenv("API_TOKEN")
security = HTTPBearer()
router = APIRouter()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=403, detail="Accès interdit")


@router.post("/clients", response_model=Client)
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


@router.get("/clients", response_model=List[Client])
def list_clients(
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(verify_token),
):
    return db.query(ClientModel).all()


@router.get("/clients/{client_id}", response_model=Client)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(verify_token),
):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client


@router.put("/clients/{client_id}", response_model=Client)
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


@router.delete("/clients/{client_id}", response_model=dict)
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
