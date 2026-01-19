import json
from app import app

def test_compute_features_success():
    client = app.test_client()

    response = client.post(
        "/compute-features",
        data=json.dumps({"values": [10, 20, 30]}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 3
    assert data["sum"] == 60
    assert data["mean"] == 20
