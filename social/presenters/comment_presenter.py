class CommentPresenter:
    def success(self, comment_id):
        return {
            "comment_id": comment_id,
            "message": "Comment created successfully",
        }

    def invalid_user(self):
        return {
            "error": "Invalid user",
        }

    def invalid_post(self):
        return {
            "error": "Invalid post",
        }

    def invalid_comment_content(self):
        return {
            "error": "Invalid comment content",
        }

    def invalid_parent_comment(self):
        return {
            "error": "Invalid parent comment",
        }

    def serialize_replies(self, replies_queryset):
        return [
            {
                "comment_id": reply.commented_id,
                "commenter": {
                    "user_id": reply.commented_by.user_id,
                    "name": reply.commented_by.name,
                    "profile_pic": reply.commented_by.profile_pic,
                },
                "commented_at": str(reply.commented_at),
                "comment_content": reply.content,
            }
            for reply in replies_queryset
        ]
