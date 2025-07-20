import os
from typing import List
from datetime import datetime, timezone
from fastapi import HTTPException, Depends, Security, APIRouter, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import Client, ClientUpdate
from app.models import ClientModel
from app.messaging.events import CUSTOMER_CREATED, CUSTOMER_UPDATED, CUSTOMER_DELETED

API_TOKEN = os.getenv("API_TOKEN")
security = HTTPBearer()
router = APIRouter()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=403, detail="Accès interdit")


async def publish_event_safe(request: Request, event_type: str, data: dict):
    """Publier un événement de manière sécurisée (ne pas faire échouer l'API si le broker est down)"""
    try:
        broker = getattr(request.app.state, "broker", None)
        if broker and broker.is_connected:
            await broker.publish_event(event_type, data)
            print(f"Event published: {event_type}")
        else:
            print(
                f"Warning: Message broker not available, event {event_type} not published"
            )
    except Exception as e:
        print(f"Error publishing event {event_type}: {str(e)}")


@router.get("/")
def read_root():
    return {"message": "API is running"}


@router.post("/clients", response_model=Client)
async def create_client(
    client: Client,
    request: Request,
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(verify_token),
):
    try:
        db_client = ClientModel(
            **client.model_dump(exclude={"id", "created_at", "updated_at"})
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)

        await publish_event_safe(
            request,
            CUSTOMER_CREATED,
            {
                "customer_id": db_client.id,
                "name": db_client.name,
                "username": db_client.username,
                "first_name": db_client.first_name,
                "last_name": db_client.last_name,
                "postal_code": db_client.postal_code,
                "city": db_client.city,
                "profile_first_name": db_client.profile_first_name,
                "profile_last_name": db_client.profile_last_name,
                "company_name": db_client.company_name,
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        return db_client

    except Exception as e:
        db.rollback()
        print(f"Error creating client: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la création du client"
        )


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
async def update_client(
    client_id: int,
    updated_client: ClientUpdate,
    request: Request,
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(verify_token),
):
    try:
        client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")

        old_values = {
            "name": client.name,
            "username": client.username,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "postal_code": client.postal_code,
            "city": client.city,
            "profile_first_name": client.profile_first_name,
            "profile_last_name": client.profile_last_name,
            "company_name": client.company_name,
        }

        changes = updated_client.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(client, field, value)

        db.commit()
        db.refresh(client)

        await publish_event_safe(
            request,
            CUSTOMER_UPDATED,
            {
                "customer_id": client.id,
                "name": client.name,
                "username": client.username,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "postal_code": client.postal_code,
                "city": client.city,
                "profile_first_name": client.profile_first_name,
                "profile_last_name": client.profile_last_name,
                "company_name": client.company_name,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "changes": changes,
                "old_values": old_values,
            },
        )

        return client

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating client: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la mise à jour du client"
        )


@router.delete("/clients/{client_id}", response_model=dict)
async def delete_client(
    client_id: int,
    request: Request,
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(verify_token),
):
    try:
        client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")

        client_data = {
            "customer_id": client.id,
            "name": client.name,
            "username": client.username,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "postal_code": client.postal_code,
            "city": client.city,
            "profile_first_name": client.profile_first_name,
            "profile_last_name": client.profile_last_name,
            "company_name": client.company_name,
            "deleted_at": datetime.now(timezone.utc).isoformat(),
        }

        db.delete(client)
        db.commit()

        await publish_event_safe(request, CUSTOMER_DELETED, client_data)

        return {"message": "Client supprimé avec succès"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting client: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la suppression du client"
        )


@router.get("/health/messaging")
async def check_messaging_health(request: Request):
    """Vérifier l'état de la connexion au message broker"""
    try:
        broker = getattr(request.app.state, "broker", None)
        if broker and broker.is_connected:
            return {
                "status": "healthy",
                "message_broker": "connected",
                "service": broker.service_name,
            }
        else:
            return {
                "status": "warning",
                "message_broker": "disconnected",
                "message": "API fonctionne mais les événements ne sont pas publiés",
            }
    except Exception as e:
        return {"status": "error", "message_broker": "error", "error": str(e)}
