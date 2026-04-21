from social.exceptions import InvalidCommentException


class GetRepliesForCommentInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_replies_for_comment(self, comment_id):
        if not self.storage.is_valid_comment(comment_id):
            raise InvalidCommentException("Invalid comment")

        return self.storage.get_replies_for_comment(comment_id)
