# RecallNote 🧠🎙️

[![CI](https://github.com/AK20202007/RecallNote/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/AK20202007/RecallNote/actions/workflows/backend-ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![SwiftUI](https://img.shields.io/badge/SwiftUI-iOS_16%2B-blue.svg?logo=swift)](https://developer.apple.com/xcode/swiftui/)

**RecallNote** is an On-Device AI Notes & Recall application. It records voice notes, transcribes them on-device, identifies speakers, generates local vector embeddings for semantic search, and syncs intelligently to a cloud backend.

By performing heavy computational tasks (transcription, embeddings, diarization) on the edge, RecallNote conserves cloud compute costs, preserves user privacy, and ensures resilience to network failures.

## 🚀 Features

- **On-Device Transcription**: Uses `whisper.cpp` (or Core ML Whisper) for fast, offline voice-to-text.
- **Voice Biometrics (Speaker Diarization)**: Automatically identifies "who said what" to build persistent speaker profiles across meetings.
- **Semantic Vector Search**: Powered by `MiniLM-L6-v2` via Core ML, allowing you to ask queries like *"What did Alice say about the budget?"*.
- **Cloud Sync**: A lightweight Python FastAPI backend that handles conflict resolution and cross-device sync.

## 📖 Architecture

For a deep dive into the system design, model trade-offs, and data flow, please read our [Architecture Document](docs/ARCHITECTURE.md).

## 🛠️ Getting Started

### 1. Backend (FastAPI + Docker)

The backend is fully containerized for easy setup. It requires Docker and Docker Compose.

```bash
cd backend
# Start the API and PostgreSQL Database
docker-compose up --build
```
The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

#### Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

### 2. iOS App (SwiftUI)

The iOS client requires macOS and Xcode 15+.

1. Open Xcode.
2. Select **Create a new Xcode project**.
3. Choose **App** under iOS and drag the contents of `ios-app/` into your project directory.
4. Run the app on a physical device (recommended for Core ML models) or the Simulator.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a Pull Request.

## 📄 License

MIT License. See `LICENSE` for details.
