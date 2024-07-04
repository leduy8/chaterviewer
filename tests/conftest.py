import pytest
from fastapi.testclient import TestClient

from app import create_app
from app.database import Base, engine
from tests.dummy_data import create_dummy_access_token, create_dummy_invalid_access_token, create_dummy_user


@pytest.fixture(scope="function")
def app():
    return create_app()


@pytest.fixture(scope="function")
def client(app):
    return TestClient(app=app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="function")
def user():
    return create_dummy_user()


@pytest.fixture(scope="function")
def access_token(user):
    return create_dummy_access_token({"uuid": user.uuid})


@pytest.fixture(scope="function")
def invalid_access_token():
    return create_dummy_invalid_access_token()
