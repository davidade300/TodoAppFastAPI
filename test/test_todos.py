"""
file for todos testing
the app will have 2 databases, one for testing and one for production
"""

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos
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


def test_read_all_authenticated(test_todo):
    """tests for all the authenticated users"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete": False, "title": "Learn to code!",
                                "description": "Need to learn everyday!",
                                "id": 1, "priority": 5, "owner_id": 1}]


def test_read_one_authenticated(test_todo):
    """tests for one of the authenticated users"""
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"complete": False, "title": "Learn to code!",
                               "description": "Need to learn everyday!",
                               "id": 1, "priority": 5, "owner_id": 1}


def test_read_one_authenticated_not_found():
    """tests for todo not found or not exists"""
    response = client.get("todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found!"}


def test_create_todo(test_todo):
    """test for a new todo"""
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")  # type: ignore
    assert model.description == request_data.get("description")  # type: ignore
    assert model.priority == request_data.get("priority")  # type: ignore
    assert model.complete == request_data.get("complete")  # type: ignore


def test_update_todo(test_todo):
    """test for updating a todo"""
    request_data = {
        "title": "Change the title of the todo already saved",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Change the title of the todo already saved"  # type:ignore


def test_update_todo_not_found(test_todo):
    """test for updating a todo"""
    request_data = {
        "title": "Change the title of the todo already saved",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found!"}


def test_delete_todo(test_todo):
    """test for deleting a todo"""
    response = client.delete("/todo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    """test for deleting a todo"""
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found!"}
