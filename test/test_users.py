"""file with tests for users"""
from fastapi import status
from routers.users import get_db, get_current_user
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    """tests for user"""
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "davidade@mail.com"
    assert response.json()["first_name"] == "David"
    assert response.json()["last_name"] == "Oliveira"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(11) 1 1111 1111"


def test_change_password_success(test_user):
    """tests for password changes"""
    response = client.put("/user/password", json={"password": "123456",
                                                  "new_password": "1234567"})

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    """tests for password changes with a invalid user"""
    response = client.put("/user/password", json={"password": "wrong_pwd",
                                                  "new_password": "1234567"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    """tests for phone number change"""
    response = client.put("/user/phone_number/222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
