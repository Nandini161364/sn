from social.models import Comment, Group, Post, User, Reaction
import uuid
from django.utils import timezone
from social.constants import reaction_types, positive_reactions, negative_reactions
from django.db.models import Count, Q, F

from social.interactors.storage_interfaces.storage_interface import StorageInterface

#Return data format should be decided by presenter, so that presenter can decide what data to send in response
class PostStorage(StorageInterface):
    def is_valid_post(self, post_id):
        return Post.objects.filter(post_id=post_id).exists()

    def is_valid_user(self, user_id):
        return User.objects.filter(user_id=user_id).exists()

    def is_valid_group(self, group_id):
        return Group.objects.filter(id=group_id).exists()

    def is_user_in_group(self, group_id, user_id):
        return Group.objects.filter(id=group_id, members__user_id=user_id).exists()
    
    def is_valid_reaction_type(self, reaction_type):
        if reaction_type not in reaction_types:
            return False
        return True

    def create_post(self, post_dto):
        post = Post.objects.create(
            post_id=str(uuid.uuid4()),
            content=post_dto.content,
            posted_by_id=post_dto.user_id,
            posted_at=timezone.now(),
            group_id=post_dto.group_id,
        )

        return post.post_id
    
    def create_reaction(self, reaction_dto):
        reaction = Reaction.objects.create(
            post_id=reaction_dto.post_id,
            reaction=reaction_dto.reaction_type,
            reacted_by_id=reaction_dto.user_id,
            reacted_at=timezone.now(),
        )
        return

    def get_existing_reaction(self, reaction_dto):
        try:
            existing_reaction = Reaction.objects.get(
                post_id=reaction_dto.post_id, 
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

    def delete_post(self, post_id):
        post = Post.objects.get(post_id=post_id)
        post.delete()
    
    def does_user_have_permission_to_delete_post(self, deletePostDto):
        return Post.objects.filter(post_id = deletePostDto.post_id, posted_by_id=deletePostDto.user_id).exists()
    

    def get_posts_with_more_positive_reactions(self):
        result = Post.objects.annotate(
            positive_count=Count('reactions', filter=Q(reactions__reaction__in=positive_reactions)),
            negative_count=Count('reactions', filter=Q(reactions__reaction__in=negative_reactions))
        ).filter(positive_count__gt=F('negative_count'))
        post_ids = result.values_list('post_id', flat=True)

        return list(post_ids)



    def get_posts_reacted_by_user(self, user_id):
        post_ids = (
            Reaction.objects.filter(reacted_by_id=user_id, post__isnull=False)
            .values_list("post_id", flat=True)
            .distinct()
        )
        return list(post_ids)

    def get_reactions_to_post(self, post_id):
        return (
            Reaction.objects.filter(post_id=post_id)
            .select_related("reacted_by")
            .order_by("reacted_at", "id")
        )

    def get_post(self, post_id):
        return (
            Post.objects.select_related("posted_by", "group")
            .prefetch_related("reactions", "comments")
            .get(post_id=post_id)
        )

    def get_user_posts(self, user_id):
        return (
            Post.objects.filter(posted_by_id=user_id)
            .select_related("posted_by", "group")
            .prefetch_related("reactions", "comments")
            .order_by("posted_at", "post_id")
        )

    def get_group_feed(self, user_id, group_id, offset, limit):
        return (
            Post.objects.filter(group_id=group_id)
            .select_related("posted_by", "group")
            .prefetch_related("reactions", "comments")
            .order_by("-posted_at", "-post_id")[offset:offset + limit]
        )

    def get_posts_with_more_comments_than_reactions(self):
        return list(
            Post.objects.annotate(
                comments_count=Count(
                    "comments",
                    filter=Q(comments__parent_comment__isnull=True),
                    distinct=True,
                ),
                reactions_count=Count("reactions", distinct=True),
            )
            .filter(comments_count__gt=F("reactions_count"))
            .values_list("post_id", flat=True)
        )
