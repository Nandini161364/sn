from social.exceptions import (
    InvalidGroupException,
    InvalidLimitSetValueException,
    InvalidOffSetValueException,
    InvalidUserException,
    UserNotInGroupException,
)


class GetGroupFeedInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def get_group_feed(self, group_feed_dto):
        if not self.storage.is_valid_user(group_feed_dto.user_id):
            raise InvalidUserException("Invalid user")

        if not self.storage.is_valid_group(group_feed_dto.group_id):
            raise InvalidGroupException("Invalid group")

        if not self.storage.is_user_in_group(group_feed_dto.group_id, group_feed_dto.user_id):
            raise UserNotInGroupException("User not in group")

        if group_feed_dto.offset < 0:
            raise InvalidOffSetValueException("Invalid offset")

        if group_feed_dto.limit <= 0:
            raise InvalidLimitSetValueException("Invalid limit")

        posts = self.storage.get_group_feed(
            user_id=group_feed_dto.user_id,
            group_id=group_feed_dto.group_id,
            offset=group_feed_dto.offset,
            limit=group_feed_dto.limit,
        )
        return self.presenter.serialize_posts(posts)
