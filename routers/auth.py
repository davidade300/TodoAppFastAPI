# pyright: reportUnboundVariable=false
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

# these two work together to add a signature to the JWT,
#  to make sure that it's secure and authorized
SECRET_KEY = "ae4bbf98c0b7b2f92d79e5b3f90602c6d4a09a1e3fe36248b9d1b96153b18644"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    pwd: str
    role: str
    phone_number: str

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "username": "davidade300",
                "email": "David@mail.com",
                "first_name": "David",
                "last_name": "Oliveira",
                "pwd": "1234356",
                "role": "admin",
                "phone_Number": "123456789"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        # yield = only the code prior to and the yield statement
        yield db
    finally:
        db.close()
        # Depends() -> dependency injection


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    # expires = datetime.utcnow() + expires_delta
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:  # payload -> data inside a token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # sub is the username in the create token fun
        username: str = payload.get("sub")  # type: ignore
        user_id: int = payload.get("id")  # type: ignore
        user_role: str = payload.get("role")  # type: ignore
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not valide user!",
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not valide user!")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        hashed_password=bcrypt_context.hash(create_user_request.pwd),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token/", response_model=Token)
async def login_for_acces_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valide user!"
        )
    token = create_access_token(
        user.username,  # type: ignore
        user.id,  # type: ignore
        user.role,  # type: ignore
        timedelta(minutes=20),
    )
    return {"access_token": token, "token_type": "bearer"}
