class ReactionPresenter:
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

    def invalid_user(self):
        return {
            "error": "Invalid user"
        }

    def invalid_post(self):
        return {
            "error": "Invalid post"
        }

    def invalid_comment(self):
        return {
            "error": "Invalid comment"
        }

    def invalid_reaction_type(self):
        return {
            "error": "Not a valid Reaction Type"
        }
