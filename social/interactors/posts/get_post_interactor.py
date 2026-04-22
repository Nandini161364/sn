from social.exceptions import InvalidPostException
from social.interactors.storage_interfaces.storage_interface import PostStorageInterface

class GetPostInteractor:
    def __init__(self, storage: PostStorageInterface, presenter):
        self.storage = storage
        self.presenter = presenter

    def get_post(self, post_id):
        if not self.storage.is_valid_post(post_id):
            raise InvalidPostException("Invalid post")

        post = self.storage.get_post(post_id)
        return self.presenter.serialize_post(post)
