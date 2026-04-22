from social.exceptions import InvalidUserException, InvalidPostException, InvalidCommentException


class CreateCommentInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_comment(self, comment_dto):
        if not self.storage.is_valid_user(comment_dto.user_id):
            raise InvalidUserException("Invalid user")

        if not self.storage.is_valid_post(comment_dto.post_id):
            raise InvalidPostException("Invalid post")

        if not comment_dto.content:
            raise InvalidCommentException("Invalid comment content")

        if comment_dto.parent_comment_id:
            if not self.storage.is_valid_comment(comment_dto.parent_comment_id):
                raise InvalidCommentException("Invalid parent comment")

            if not self.storage.is_comment_in_post(
                comment_id=comment_dto.parent_comment_id,
                post_id=comment_dto.post_id,
            ):
                raise InvalidCommentException("Parent comment not in post")

        comment_id = self.storage.create_comment(comment_dto)
        return self.presenter.success(comment_id)
