"""file with tests for auth"""
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
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