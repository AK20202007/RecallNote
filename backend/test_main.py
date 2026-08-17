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

def test_sync_multiple_notes():
    now = datetime.now(timezone.utc).isoformat()
    payload = [
        {
            "id": str(uuid.uuid4()),
            "text_content": "Note 1",
            "created_at": now,
            "updated_at": now
        },
        {
            "id": str(uuid.uuid4()),
            "text_content": "Note 2",
            "created_at": now,
            "updated_at": now
        }
    ]
    response = client.post("/sync/notes", json=payload)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_conflict_resolution():
    now = datetime.now(timezone.utc)
    older = now.isoformat()
    newer = datetime(now.year, now.month, now.day, now.hour, now.minute + 5, tzinfo=timezone.utc).isoformat()
    note_id = str(uuid.uuid4())
    
    # Sync older version
    client.post("/sync/notes", json=[{
        "id": note_id,
        "text_content": "Old Content",
        "created_at": older,
        "updated_at": older
    }])
    
    # Sync newer version
    res_newer = client.post("/sync/notes", json=[{
        "id": note_id,
        "text_content": "New Content",
        "created_at": older,
        "updated_at": newer
    }])
    assert res_newer.json()[0]["text_content"] == "New Content"
    
    # Attempt to sync older version again, should be ignored (last write wins)
    client.post("/sync/notes", json=[{
        "id": note_id,
        "text_content": "Old Content AGAIN",
        "created_at": older,
        "updated_at": older
    }])
    
    final_res = client.get("/notes")
    note = next(n for n in final_res.json() if n["id"] == note_id)
    assert note["text_content"] == "New Content"
