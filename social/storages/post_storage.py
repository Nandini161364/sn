from social.models import Comment, Group, Post, User, Reaction
import uuid
from django.utils import timezone
from social.constants import reaction_types, positive_reactions, negative_reactions
from django.db.models import Count, Q, F

class PostStorage:
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

    def _get_reaction_summary(self, reactions_queryset):
        reaction_types = list(
            reactions_queryset.values_list("reaction", flat=True).distinct()
        )
        return {
            "count": reactions_queryset.count(),
            "type": reaction_types,
        }

    def _serialize_reply(self, reply):
        return {
            "comment_id": reply.commented_id,
            "commenter": {
                "user_id": reply.commented_by.user_id,
                "name": reply.commented_by.name,
                "profile_pic": reply.commented_by.profile_pic,
            },
            "commented_at": str(reply.commented_at),
            "comment_content": reply.content,
            "reactions": self._get_reaction_summary(reply.reactions.all()),
        }

    def _serialize_comment(self, comment):
        replies = list(
            Comment.objects.filter(parent_comment_id=comment.commented_id)
            .select_related("commented_by")
            .prefetch_related("reactions")
            .order_by("commented_at", "commented_id")
        )
        return {
            "comment_id": comment.commented_id,
            "commenter": {
                "user_id": comment.commented_by.user_id,
                "name": comment.commented_by.name,
                "profile_pic": comment.commented_by.profile_pic,
            },
            "commented_at": str(comment.commented_at),
            "comment_content": comment.content,
            "reactions": self._get_reaction_summary(comment.reactions.all()),
            "replies_count": len(replies),
            "replies": [self._serialize_reply(reply) for reply in replies],
        }

    def _serialize_post(self, post):
        comments = list(
            Comment.objects.filter(post_id=post.post_id, parent_comment__isnull=True)
            .select_related("commented_by")
            .prefetch_related("reactions")
            .order_by("commented_at", "commented_id")
        )
        return {
            "post_id": post.post_id,
            "group": (
                {
                    "group_id": post.group.id,
                    "name": post.group.name,
                }
                if post.group_id
                else None
            ),
            "posted_by": {
                "name": post.posted_by.name,
                "user_id": post.posted_by.user_id,
                "profile_pic": post.posted_by.profile_pic,
            },
            "posted_at": str(post.posted_at),
            "post_content": post.content,
            "reactions": self._get_reaction_summary(post.reactions.all()),
            "comments": [self._serialize_comment(comment) for comment in comments],
            "comments_count": Comment.objects.filter(post_id=post.post_id).count(),
        }

    def get_posts_reacted_by_user(self, user_id):
        post_ids = (
            Reaction.objects.filter(reacted_by_id=user_id, post__isnull=False)
            .values_list("post_id", flat=True)
            .distinct()
        )
        return list(post_ids)

    def get_reactions_to_post(self, post_id):
        reactions = (
            Reaction.objects.filter(post_id=post_id)
            .select_related("reacted_by")
            .order_by("reacted_at", "id")
        )
        return [
            {
                "user_id": reaction.reacted_by.user_id,
                "name": reaction.reacted_by.name,
                "profile_pic": reaction.reacted_by.profile_pic,
                "reaction": reaction.reaction,
            }
            for reaction in reactions
        ]

    def get_post(self, post_id):
        post = (
            Post.objects.select_related("posted_by", "group")
            .prefetch_related("reactions")
            .get(post_id=post_id)
        )
        return self._serialize_post(post)

    def get_user_posts(self, user_id):
        posts = (
            Post.objects.filter(posted_by_id=user_id)
            .select_related("posted_by", "group")
            .prefetch_related("reactions")
            .order_by("posted_at", "post_id")
        )
        return [self._serialize_post(post) for post in posts]

    def get_group_feed(self, user_id, group_id, offset, limit):
        posts = (
            Post.objects.filter(group_id=group_id)
            .select_related("posted_by", "group")
            .prefetch_related("reactions")
            .order_by("-posted_at", "-post_id")[offset:offset + limit]
        )
        return [self._serialize_post(post) for post in posts]

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
