def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["message"] == "API working correctly"
    assert data["version"] == "1.0.0"
    assert data["database"] == "connected"

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sicoob API"
    assert data["version"] == "1.0.0"
    assert "docs" in data
    assert "health" in data
