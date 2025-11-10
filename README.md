# SnapLite API — FastAPI Photo/Video Upload Backend

SnapLite is a minimal media-sharing backend built with **FastAPI**. It accepts image/video uploads with captions and returns a public **feed** plus direct **media URLs**. Perfect starter for social features, UGC portals, or lightweight CMS backends.

## Features
- `POST /upload` — Upload an image or short video with `username` and `caption`
- `GET /feed` — Reverse-chronological list of posts (username, caption, media_url, timestamp)
- `/media/...` — Serves uploaded files directly (mounted static directory)
- Typed models (Pydantic) + auto-docs via Swagger (`/docs`)

## Tech Stack
- Python 3.12 • FastAPI • Uvicorn • Pydantic
- Local disk storage (swap to S3/Supabase/Postgres easily)
- Clean, modular structure (`models.py`, `storage.py`, `main.py`)

## Run Locally
```bash
python -m venv venv
# Windows
venv\Scripts\Activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
