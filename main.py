import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles

from models import Post
from storage import store

app = FastAPI(
    title = "SnapLite API",
    description = "Minimal media sharing backend (photo/video upload + public feed)",
    version = "1.0.0"
)

# --- Make sure uploads folder exists and serve it publicly ---
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

# This mounts /media so files in ./uploads can be accessed in browser
app.mount("/media", StaticFiles(directory = UPLOAD_DIR), name = "media")


@app.get("/", tags = ["health"])
def health_check():
    return {"status": "ok"}

@app.get("/feed", response_model=List[Post], tags = ["posts"])
def get_feed():
    """
    Public feed of recent photo/video posts.

    """
    # newest first
    return store.get_feed()

@app.post("/upload", response_model = Post, tags = ["posts"])
async def upload_post(
    username: str = Form(...),
    caption: str = Form(""),
    file: UploadFile = File(...)
):
    """
    Create a new post by uploading an image or video.
    Returns the created Post.

    """

    # 1. validate file type
    allowed_types = [
        "image/jpeg", "image/png", "image/webp",
        "video/mp4", "video/quicktime", "video/x-matroska"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code = 400, detail = "Unsupported file type")
    
    # 2. Build a safe file name for disk
    # Give it a unique ID based on the next post ID, keep extension
    _, ext = os.path.splitext(file.filename)
    if not ext:
        # fallback if upload has no extension
        if "image" in file.content_type:
            ext = ".jpg"
        elif "video" in file.content_type:
            ext = ".mp4"
        else:
            ext = ".bin"

    filename = f"post_{len(store.get_feed()) + 1}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 3. save uploaded file bytes to disk
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 4. Generate URL tht clients/frontends can use
    media_url = f"/media/{filename}"

    # 5. create the Post object and store it
    post = store.add_post(
        username = username,
        caption = caption,
        media_url = media_url
    )

    return post