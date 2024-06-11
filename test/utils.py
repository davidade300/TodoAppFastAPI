"""file with all the reusable code"""
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from database import Base
from main import app
from models import Todos, Users
from routers.auth import bcrypt_context

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
    return {"username": "davidade300", "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture(name="test_todo")
def test_todo():
    """fixture for todos testing"""
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo  # yield makes it  run till the end of the function
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture(name="test_user")
def test_user():
    """fixture for user testing"""
    user = Users(
        username="davidade300",
        email="davidade@mail.com",
        first_name="David",
        last_name="Oliveira",
        hashed_password=bcrypt_context.hash("123456"),
        phone_number="(11) 1 1111 1111",
        role="admin"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
