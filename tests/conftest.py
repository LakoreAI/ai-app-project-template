import pytest
from fastapi.testclient import TestClient

import src


@pytest.fixture
def client():
    with TestClient(src.create_app()) as c:
        yield c
