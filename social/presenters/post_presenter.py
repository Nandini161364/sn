class PostPresenter:

    def success(self, post_id):
        return {
            "post_id": post_id,
            "message": "Post created successfully"
        }

    def invalid_user(self):
        return {
            "error": "Invalid user"
        }

    def invalid_post(self):
        return {
            "error": "Invalid post"
        }

    def invalid_group(self):
        return {
            "error": "Invalid group"
        }

    def user_not_in_group(self):
        return {
            "error": "User not in group"
        }

    def invalid_reaction(self):
        return {
            "error": "Not a valid Reaction Type"
        }

    def reaction_created(self):
        return {
            "message": "Reaction created successfully"
        }

    def reaction_deleted(self):
        return {
            "message": "Reaction removed successfully"
        }

    def reaction_updated(self):
        return {
            "message": "Reaction updated successfully"
        }
    def user_cannot_delete_post(self):
        return{
            "message": "User doesn't have permission to delete post"
        }
    def post_deleted(self):
        return {
            "message": "Post Deleted Successfully"
        }

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
        from social.models import Comment
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
        from social.models import Comment
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

    def serialize_reactions_to_post(self, reactions_queryset):
        return [
            {
                "user_id": reaction.reacted_by.user_id,
                "name": reaction.reacted_by.name,
                "profile_pic": reaction.reacted_by.profile_pic,
                "reaction": reaction.reaction,
            }
            for reaction in reactions_queryset
        ]

    def serialize_post(self, post):
        return self._serialize_post(post)

    def serialize_posts(self, posts_queryset):
        return [self._serialize_post(post) for post in posts_queryset]