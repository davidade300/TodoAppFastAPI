"""test for the main.py file endpoint"""

from fastapi.testclient import TestClient  # creates a test client
from fastapi import status
from ..main import app

client = TestClient(app)


def test_return_health_check():
    """test for the endpoint"""
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
