from sqlalchemy import Column, Integer, String
from app.db import Base


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
