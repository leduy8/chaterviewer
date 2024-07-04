from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from app.models.users import User
from app.schemas.auth import SignUpRequest
from app.schemas.users import UserRequest
from app.utils.password import gen_salt, generate_password_hash


def find_user_by_uuid(db: Session, uuid: str):
    return db.query(User).filter_by(uuid=uuid).first()


def find_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).first()


def create_user(db: Session, data: SignUpRequest):
    if find_user_by_email(db, email=data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email={data.email} existed",
        )

    salt = gen_salt()
    password_hash = generate_password_hash(password=data.password, salt=salt)

    user = User(email=data.email, password_hash=password_hash, name=data.name, salt=salt)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, uuid: int, data: UserRequest):
    user = db.query(User).filter_by(uuid=uuid).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user.name = data.name

    db.commit()

    return user
