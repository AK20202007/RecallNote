# RecallNote Technical Architecture

This document serves as a reference for interviews, outlining the system architecture, model choices, sync strategies, and data flow of the **RecallNote** application.

## Overview

RecallNote is an On-Device AI Notes & Recall application. It records voice notes, transcribes them on-device, generates local vector embeddings for semantic search, and syncs intelligently to a cloud backend. 

### Why this Architecture?

Most LLM applications simply act as a wrapper around an OpenAI API call. RecallNote is engineered to demonstrate the real trade-offs and constraints of running AI locally on mobile devices. By performing heavy computational tasks (transcription, embeddings) on the device edge, we conserve cloud compute costs, preserve user privacy, and ensure the app is resilient to network failures.

## 1. Native iOS Client (Swift / SwiftUI)

The mobile client is responsible for UI, local ML inference, and offline storage.

### Model Choices (On-Device ML)
- **Transcription**: `whisper.cpp` (quantized models) or **Core ML Whisper** 
  - *Trade-off*: We utilize a small, quantized Whisper model (e.g., `tiny` or `base`) to balance accuracy with memory constraints and battery consumption. 
- **Speaker Diarization & Biometrics**: Lightweight on-device clustering model (e.g., optimized `pyannote.audio` or Apple's Speech framework).
  - *Trade-off*: Adds minor memory overhead but enables building persistent speaker profiles ("Voice Prints") across meetings. This massively increases the utility of recall (e.g., "what did *Alice* say about the budget?").
- **Embeddings**: `MiniLM-L6-v2` via **Core ML** (SentenceTransformers).
  - *Trade-off*: The embedding model maps transcribed text to dense vectors. By keeping this small (~20MB), we achieve fast semantic search (cosine similarity) without cloud latency.

### Data Flow (Local)
1. User records audio via `AVFoundation`.
2. Audio stream is buffered and passed to the local Whisper model for raw transcription.
3. Concurrently, the audio passes through the Speaker Diarization model to identify speaker turns and map them to persistent local Voice Prints (e.g., Speaker 1 -> Alice).
4. The transcript is segmented by speaker. These segments are passed to the local SentenceTransformer to generate multi-dimensional float arrays (embeddings).
5. Text segments (with `speaker_id`), embeddings, and speaker profiles are stored in local **Core Data** (or Realm).
6. User queries are embedded locally and compared against stored note embeddings via Cosine Similarity for fast semantic recall, which can now be filtered by speaker.

## 2. Cloud Backend & Sync (Python / FastAPI)

The backend acts as a source of truth for multi-device sync, auth, and complex summarization fallback.

### Tech Stack
- **API**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with `pgvector`.
- **Infrastructure**: Docker & Docker Compose.

### Sync Strategy
- **Conflict Resolution**: The system uses a Last-Write-Wins (LWW) mechanism based on the `updated_at` timestamp. In a more advanced iteration, this could transition to CRDTs (Conflict-free Replicated Data Types) for real-time collaborative editing.
- **Background Sync**: The iOS app uses Background Tasks (`BGTaskScheduler`) to silently sync notes to the FastAPI endpoint when the device is plugged in and on Wi-Fi, saving battery.

### Optional Cloud LLM Fallback
- While transcription and basic recall are completely offline, summarization (e.g., extracting action items from a 30-minute meeting) is memory-intensive.
- If the device is online, it sends the transcript to the FastAPI backend, which makes a lightweight API call to OpenAI (GPT-4o-mini) to generate a summary. This demonstrates the ability to reason about hybrid edge-cloud AI architectures.
