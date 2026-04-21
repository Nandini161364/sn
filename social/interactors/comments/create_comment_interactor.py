class CreateCommentInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_comment(self, comment_dto):
        if not self.storage.is_valid_user(comment_dto.user_id):
            return self.presenter.invalid_user()

        if not self.storage.is_valid_post(comment_dto.post_id):
            return self.presenter.invalid_post()

        if not comment_dto.content:
            return self.presenter.invalid_comment_content()

        if comment_dto.parent_comment_id:
            if not self.storage.is_valid_comment(comment_dto.parent_comment_id):
                return self.presenter.invalid_parent_comment()

            if not self.storage.is_comment_in_post(
                comment_id=comment_dto.parent_comment_id,
                post_id=comment_dto.post_id,
            ):
                return self.presenter.invalid_parent_comment()

        comment_id = self.storage.create_comment(comment_dto)
        return self.presenter.success(comment_id)
