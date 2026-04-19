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
            "error": "Invalid post content"
        }