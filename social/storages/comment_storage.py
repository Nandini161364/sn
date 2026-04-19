import uuid

from django.utils import timezone

from social.models import Comment, Post, User


class CommentStorage:
    def is_valid_post(self, post_id):
        return Post.objects.filter(post_id=post_id).exists()

    def is_valid_user(self, user_id):
        return User.objects.filter(user_id=user_id).exists()

    def create_comment(self, comment_dto):
        comment = Comment.objects.create(
            commented_id=str(uuid.uuid4()),
            content=comment_dto.content,
            commented_by_id=comment_dto.user_id,
            commented_at=timezone.now(),
            post_id=comment_dto.post_id,
        )
        return comment.commented_id
