from social.exceptions import (
    InvalidGroupException,
    InvalidPostException,
    InvalidUserException,
    UserNotInGroupException,
)


class CreatePostInteractor:

    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_post(self, post_dto):
        if not self.storage.is_valid_user(post_dto.user_id):
            raise InvalidUserException("Invalid user")

        if not post_dto.content:
            raise InvalidPostException("Invalid post")

        if post_dto.group_id:
            if not self.storage.is_valid_group(post_dto.group_id):
                raise InvalidGroupException("Invalid group")

            if not self.storage.is_user_in_group(post_dto.group_id, post_dto.user_id):
                raise UserNotInGroupException("User not in group")

        post_id = self.storage.create_post(post_dto)

        return self.presenter.success(post_id)
    