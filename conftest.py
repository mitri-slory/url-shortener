import pytest
from urlshort import create_app

#Fixtures help establish testing
@pytest.fixture
def app():
    app = create_app()
    yield app

#Fixture to get a client 
@pytest.fixture
def client(app):
    return app.test_client()
