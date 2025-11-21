from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app=app)


def test_read_main():
  response = client.post(
    "/tenants",
    json={
      "name": "Delta Technologies",
      "domain": "delta-tech.com",
      "plan": "enterprise"
    })

  assert response.status_code == 201

  data = response.json()
  assert data["name"] == "Delta Technologies"
  assert data["domain"] == "delta-tech.com"
  assert data["plan"] == "enterprise"