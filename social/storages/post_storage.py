from social.models import Post
import uuid
from django.utils import timezone

class PostStorage:

    def create_post(self, post_dto):
        post = Post.objects.create(
            post_id=str(uuid.uuid4()),
            content=post_dto.content,
            posted_by_id=post_dto.user_id,
            posted_at=timezone.now()
        )

        return post.post_id