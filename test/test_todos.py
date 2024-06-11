"""
file for todos testing
the app will have 2 databases, one for testing and one for production
"""

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status
from database import Base
from main import app
from routers.todos import get_db, get_current_user


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """func to override the default get_db"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    """func to override the default get_current_user"""
    return {"username": "davidadetest", "id": 1, "user_role": "admin"}


# this forces the application in a way that when it runs it will be ran as a test
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_read_all_authenticated():
    """tests for all the authenticated users"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
