from social.exceptions import InvalidPostException


class GetReactionsToPostInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def get_reactions_to_post(self, post_id):
        if not self.storage.is_valid_post(post_id):
            raise InvalidPostException("Invalid post")

        reactions = self.storage.get_reactions_to_post(post_id)
        return self.presenter.serialize_reactions_to_post(reactions)
