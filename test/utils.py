"""file with all the reusable code"""
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
import pytest
from models import Todos

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


client = TestClient(app)


@pytest.fixture(name="test_todo")
def todo_fixture():
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
