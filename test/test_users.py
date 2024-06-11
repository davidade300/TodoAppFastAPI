"""file with tests for users"""
from fastapi import status
from routers.users import get_db, get_current_user
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    """test for user"""
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "davidade@mail.com"
    assert response.json()["first_name"] == "David"
    assert response.json()["last_name"] == "Oliveira"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(11) 1 1111 1111"
