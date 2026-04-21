from social.exceptions import InvalidUserException


class GetUserPostsInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_user_posts(self, user_id):
        if not self.storage.is_valid_user(user_id):
            raise InvalidUserException("Invalid user")

        return self.storage.get_user_posts(user_id)
