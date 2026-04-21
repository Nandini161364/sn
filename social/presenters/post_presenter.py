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