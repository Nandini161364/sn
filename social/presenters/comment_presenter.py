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
