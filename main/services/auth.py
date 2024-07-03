from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from main.models.users import User
from main.schemas.auth import LoginRequest, SignUpRequest
from main.services import users as user_service
from main.utils.jwt import create_access_token
from main.utils.password import check_password_hash


def signup(db: Session, data: SignUpRequest):
    return user_service.create_user(db, data)


def login(db: Session, data: LoginRequest):
    user = db.query(User).filter_by(email=data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")

    if not check_password_hash(password_hash=user.password_hash, password=data.password, salt=user.salt):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")

    return {"access_token": create_access_token({"uuid": user.uuid})}
