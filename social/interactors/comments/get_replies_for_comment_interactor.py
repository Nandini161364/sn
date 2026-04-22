from social.exceptions import InvalidCommentException


class GetRepliesForCommentInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def get_replies_for_comment(self, comment_id):
        if not self.storage.is_valid_comment(comment_id):
            raise InvalidCommentException("Invalid comment")

        replies = self.storage.get_replies_for_comment(comment_id)
        return self.presenter.serialize_replies(replies)
