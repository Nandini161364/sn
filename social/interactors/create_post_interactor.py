class CreatePostInteractor:

    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_post(self, post_dto):

        if not post_dto.user_id:
            return self.presenter.invalid_user()

        if not post_dto.content:
            return self.presenter.invalid_post()

        post_id = self.storage.create_post(post_dto)

        return self.presenter.success(post_id)