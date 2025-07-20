import os
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
import aio_pika

from app.db import Base, engine
from app.routes import router as client_router
from app.messaging.broker import MessageBroker

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:password@rabbitmq:5672/")
SERVICE_NAME = "customer-api"

broker = MessageBroker(RABBITMQ_URL, SERVICE_NAME)


async def handle_external_events(message: aio_pika.IncomingMessage):
    """Handler pour les événements provenant des autres services"""
    async with message.process():
        try:
            event = json.loads(message.body.decode())
            event_type = event.get("event_type")
            data = event.get("data", {})

            print(f"📨 Received event: {event_type} from {event.get('service')}")

            if event_type == "product.updated":
                print(f"Product updated: {data.get('product_id')}")

            elif event_type == "order.created":
                customer_id = data.get("customer_id")
                print(f"New order created for customer: {customer_id}")

            elif event_type == "order.cancelled":
                customer_id = data.get("customer_id")
                print(f"Order cancelled for customer: {customer_id}")

        except json.JSONDecodeError:
            print("Error: Invalid JSON in message")
        except Exception as e:
            print(f"Error processing event: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Customer API...")

    Base.metadata.create_all(bind=engine)
    print("Database tables created")

    try:
        # Add debug logging to see what URL is being used
        print(f"🔗 Attempting to connect to RabbitMQ: {RABBITMQ_URL}")

        await broker.connect()
        print("Connected to message broker")

        await broker.subscribe_to_events(
            event_patterns=[
                "product.updated",
                "product.deleted",
                "order.created",
                "order.updated",
                "order.cancelled",
            ],
            callback=handle_external_events,
        )
        print("Subscribed to external events")

    except Exception as e:
        print(f"Failed to connect to message broker: {str(e)}")
        print(f"Debug: RABBITMQ_URL = {RABBITMQ_URL}")

    app.state.broker = broker

    yield

    print("Shutting down Customer API...")
    if broker.connection and not broker.connection.is_closed:
        await broker.connection.close()
        print("Message broker connection closed")


app = FastAPI(
    title="API Gestion des Clients",
    description="API REST pour la gestion des clients PayeTonKawa",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(client_router)


@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé"""
    broker_status = (
        "connected"
        if broker.connection and not broker.connection.is_closed
        else "disconnected"
    )
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "message_broker": broker_status,
    }
