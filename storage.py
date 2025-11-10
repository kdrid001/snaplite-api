from typing import List
from datetime import datetime
from models import Post 

class FeedStore:
    def __init__(self):
        self._posts: List[Post] = []
        self._next_id: int = 1

    def add_post(self, username: str, caption: str, media_url: str) -> Post:
        post = Post(
            post_id = self._next_id,
            username = username,
            caption = caption,
            media_url = media_url,
            created_at = datetime.utcnow()
        )
        self._posts.append(post)
        self._next_id +=1
        return post
    
    def get_feed(self) -> List[Post]:
        # Newest first
        return list(reversed(self._posts))
    
# Create one global store instance
store = FeedStore()