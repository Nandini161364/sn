from social.exceptions import InvalidPostException

class GetReactionMetricsInteractor:
    def __init__(self, storage):
        self.storage = storage
        # self.presenter = self.presenter

    def get_reaction_metrics(self, post_id):
        if not self.storage.is_valid_post(post_id):
            raise InvalidPostException("invalid post")

        return self.storage.get_reaction_metrics(post_id)