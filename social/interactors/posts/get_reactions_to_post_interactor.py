from social.exceptions import InvalidPostException


class GetReactionsToPostInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_reactions_to_post(self, post_id):
        if not self.storage.is_valid_post(post_id):
            raise InvalidPostException("Invalid post")

        return self.storage.get_reactions_to_post(post_id)
