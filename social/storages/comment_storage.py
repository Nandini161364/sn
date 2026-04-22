import uuid

from django.utils import timezone

from social.models import Comment, Post, User, Reaction
from social.constants import reaction_types


class CommentStorage:
    def is_valid_post(self, post_id):
        return Post.objects.filter(post_id=post_id).exists()

    def is_valid_user(self, user_id):
        return User.objects.filter(user_id=user_id).exists()

    def is_valid_comment(self, comment_id):
        return Comment.objects.filter(commented_id=comment_id).exists()

    def is_comment_in_post(self, comment_id, post_id):
        return Comment.objects.filter(commented_id=comment_id, post_id=post_id).exists()

    def get_post_id_for_comment(self, comment_id):
        comment = Comment.objects.filter(commented_id=comment_id).only("post_id").first()
        if not comment:
            return None
        return comment.post_id

    def create_comment(self, comment_dto):
        comment = Comment.objects.create(
            commented_id=str(uuid.uuid4()),
            content=comment_dto.content,
            commented_by_id=comment_dto.user_id,
            commented_at=timezone.now(),
            post_id=comment_dto.post_id,
            parent_comment_id=comment_dto.parent_comment_id,
        )
        return comment.commented_id

    def is_valid_reaction_type(self, reaction_type):
        if reaction_type not in reaction_types:
            return False
        return True

    def create_reaction(self, reaction_dto):
        reaction = Reaction.objects.create(
            comment_id=reaction_dto.comment_id,
            reaction=reaction_dto.reaction_type,
            reacted_by_id=reaction_dto.user_id,
            reacted_at=timezone.now(),
        )
        return

    def get_existing_reaction(self, reaction_dto):
        try:
            existing_reaction = Reaction.objects.get(
                comment_id=reaction_dto.comment_id,
                reacted_by_id=reaction_dto.user_id
            )
            return {
                'reaction_id': existing_reaction.id,
                'reaction': existing_reaction.reaction
            }
        except Reaction.DoesNotExist:
            return None

    def delete_reaction(self, reaction_id):
        reaction = Reaction.objects.get(id=reaction_id)
        reaction.delete()

    def update_reaction(self, reaction_id, reaction_type):
        reaction = Reaction.objects.get(id=reaction_id)
        reaction.reaction = reaction_type
        reaction.reacted_at = timezone.now()
        reaction.save()

    def get_replies_for_comment(self, comment_id):
        return (
            Comment.objects.filter(parent_comment_id=comment_id)
            .select_related("commented_by")
            .prefetch_related("reactions")
            .order_by("commented_at", "commented_id")
        )
