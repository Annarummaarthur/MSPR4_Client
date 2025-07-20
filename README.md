# API Client - PayeTonKawa

API REST pour la gestion des clients dans l'architecture microservices de PayeTonKawa.

## 🚀 Installation

### Prérequis

- Docker et Docker Compose
- Base de données Supabase configurée
- Python 3.11+ (pour le développement local)

### Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql://postgres:VOTRE_PASSWORD@db.kziubeguijtomrtufrlm.supabase.co:5432/postgres?sslmode=require
API_TOKEN=supersecrettoken123
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=password
RABBITMQ_URL=amqp://admin:password@rabbitmq:5672/
```

### Lancement avec Docker Compose

```bash
# Cloner le projet
git clone https://github.com/Annarummaarthur/MSPR4_Client
cd MSPR4_Client

# Lancer les services
docker-compose up
```

## 📋 Structure de la base de données

### Table `clients`

```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    username VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    postal_code VARCHAR,
    city VARCHAR,
    profile_first_name VARCHAR,
    profile_last_name VARCHAR,
    company_name VARCHAR,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔧 Services inclus

- **API FastAPI** : Port 8000
- **RabbitMQ** : Port 5672 (Management: 15672)
- **PostgreSQL** : Port 5433 (pour CI/tests)

## 📖 Documentation API

Une fois lancé, accéder à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔐 Authentification

Toutes les routes (sauf `/` et `/health`) nécessitent un token Bearer :

```bash
Authorization: Bearer supersecrettoken123
```

## 📝 Endpoints disponibles

### Clients

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Status de l'API |
| GET | `/clients` | Liste tous les clients |
| GET | `/clients/{id}` | Récupère un client |
| POST | `/clients` | Crée un nouveau client |
| PUT | `/clients/{id}` | Met à jour un client |
| DELETE | `/clients/{id}` | Supprime un client |

### Santé

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Santé générale |
| GET | `/health/messaging` | Santé du message broker |

## 📊 Exemple de données

### Création d'un client

```json
{
  "name": "Jean Dupont",
  "username": "jean.dupont",
  "first_name": "Jean",
  "last_name": "Dupont",
  "postal_code": "75001",
  "city": "Paris",
  "profile_first_name": "Jean-Claude",
  "profile_last_name": "Durand",
  "company_name": "ACME Corp"
}
```

## 🔄 Events publié

L'API publie automatiquement des événements via RabbitMQ :

- `customer.created` : Client créé
- `customer.updated` : Client mis à jour  
- `customer.deleted` : Client supprimé

### Format des événements

```json
{
  "event_type": "customer.created",
  "event_id": "uuid",
  "timestamp": "2025-01-20T18:30:00Z",
  "service": "customer-api",
  "data": {
    "customer_id": 1,
    "name": "Jean Dupont",
    "created_at": "2025-01-20T18:30:00Z"
  }
}
```

## 📥 Events consommés

L'API écoute les événements des autres services :

- `product.updated`
- `product.deleted`
- `order.created`
- `order.updated`
- `order.cancelled`

## 🛠️ Développement

### Installation locale

```bash
# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer en mode développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

## 🚨 Dépannage

### Erreur de connexion à la base

1. Vérifier que Supabase est accessible
2. Vérifier les credentials dans `.env`
3. Vérifier que la table `clients` existe avec la bonne structure

## 📁 Structure du projet

```
MSPR4_Client/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── db.py                # Configuration base de données
│   ├── models.py            # Modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   ├── routes.py            # Routes API
│   └── messaging/
│       ├── __init__.py
│       ├── broker.py        # Client RabbitMQ
│       └── events.py        # Définitions événements
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```
