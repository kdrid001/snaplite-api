from pydantic import BaseModel, Field
from datetime import datetime

class Post(BaseModel):
    post_id: int = Field(..., description="Unique ID for the post")
    username: str = Field(..., min_length=2, max_length=30)
    caption: str = Field(..., max_length=2200)
    media_url: str = Field(..., description="Path to uploaded photo or video")
    created_at: datetime = Field(default_factory=datetime.utcnow)
