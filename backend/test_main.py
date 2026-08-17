from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timezone
import uuid

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_sync_notes():
    now = datetime.now(timezone.utc).isoformat()
    note_id = str(uuid.uuid4())
    payload = [{
        "id": note_id,
        "text_content": "This is a test note.",
        "speaker_id": str(uuid.uuid4()),
        "embedding": [0.1, 0.2, 0.3],
        "created_at": now,
        "updated_at": now
    }]
    
    response = client.post("/sync/notes", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == note_id
    assert data[0]["text_content"] == "This is a test note."

def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
