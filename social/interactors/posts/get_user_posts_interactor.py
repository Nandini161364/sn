from social.exceptions import InvalidUserException


class GetUserPostsInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def get_user_posts(self, user_id):
        if not self.storage.is_valid_user(user_id):
            raise InvalidUserException("Invalid user")

        posts = self.storage.get_user_posts(user_id)
        return self.presenter.serialize_posts(posts)
