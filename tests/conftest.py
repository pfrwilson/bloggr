import fastapi
import pytest
from fastapi.testclient import TestClient
from bloggr import get_app
from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def app():
    
    app = get_app(
        config = {"database_url": "sqlite:///.test.db"}
    )
    yield app
    
    app.state.db['metadata'].drop_all()


@pytest.fixture
def client(app):
    return TestClient(app)






