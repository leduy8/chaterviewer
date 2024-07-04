from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.models import User
from app.utils.jwt import create_access_token
from app.utils.password import gen_salt, generate_password_hash

Session = sessionmaker(bind=engine)
session = Session()


def create_dummy_email(local_part_length=50, domain_part_length=250):
    return "".join("a" for _ in range(local_part_length)) + "@" + "".join("a" for _ in range(domain_part_length))


def create_dummy_text(length=60):
    return "".join("a" for _ in range(length))


def create_dummy_access_token(payload):
    return create_access_token(payload)


def create_dummy_user(email="duy123@gmail.com", password="Duy123456!", name="duy"):
    data = {"email": email, "password": password, "name": name}

    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        session.delete(existing_user)
        session.commit()

    salt = gen_salt()
    password_hash = generate_password_hash(password=data["password"], salt=salt)

    user = User(email=data["email"], password_hash=password_hash, name=data["name"], salt=salt)

    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()

    return user


def create_dummy_invalid_access_token(payload={"uuid": 1234}, key="dumbkey"):
    return create_access_token(payload=payload, key=key)
