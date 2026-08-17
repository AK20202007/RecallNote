from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="RecallNote API")

class NoteBase(BaseModel):
    text_content: str
    speaker_id: Optional[str] = None
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime

class NoteCreate(NoteBase):
    id: str

class Note(NoteBase):
    id: str

# In-memory store for demonstration purposes
notes_db = {}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/sync/notes", response_model=List[Note])
def sync_notes(notes: List[NoteCreate]):
    """
    Basic sync endpoint. In a real application, this would handle
    conflict resolution (e.g., using CRDTs or last-write-wins based on updated_at)
    and store notes in a PostgreSQL database with pgvector for embeddings.
    """
    synced_notes = []
    for note in notes:
        # Simple last-write-wins logic
        if note.id not in notes_db or note.updated_at > notes_db[note.id].updated_at:
            notes_db[note.id] = note
            synced_notes.append(note)
    return synced_notes

@app.get("/notes", response_model=List[Note])
def get_notes():
    return list(notes_db.values())
