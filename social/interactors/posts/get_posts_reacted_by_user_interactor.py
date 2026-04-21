from social.exceptions import InvalidUserException


class GetPostsReactedByUserInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_posts_reacted_by_user(self, user_id):
        if not self.storage.is_valid_user(user_id):
            raise InvalidUserException("Invalid user")

        return self.storage.get_posts_reacted_by_user(user_id)
