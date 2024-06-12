"""file with tests for auth"""
from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from routers.auth import (ALGORITHM, SECRET_KEY, authenticate_user,
                          create_access_token, get_current_user, get_db)

from .utils import *

app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_user):
    """tests for user authentication"""
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "123456", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username  # type: ignore

    non_existent_user = authenticate_user("WrongUserName", "123456", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "654321", db)
    assert wrong_password_user is False


def test_create_access_token():
    """tests for creating an access token"""
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={"verify_signature": False})

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio  # marks the function as an async application
async def test_get_current_user_valid_token():
    """
    when testing for an async function you should
    use a async test function
    """

    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    # since get_current_user is asyn you should use await
    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    """
    test for --if-- an exception happens calls the exception
    that says that the user is not validated
    """
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not valide user!"
