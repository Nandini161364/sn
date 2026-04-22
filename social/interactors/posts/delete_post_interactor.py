class DeletePostInteractor:
    
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def delete_post(self, deletePostDto):
        user_id = deletePostDto.user_id
        post_id = deletePostDto.post_id

        if not self.storage.is_valid_user(user_id):
            return self.presenter.invalid_user()
        if not self.storage.is_valid_post(post_id):
            return self.presenter.invalid_post()
        if not self.storage.does_user_have_permission_to_delete_post(deletePostDto):
            return self.presenter.user_cannot_delete_post()
        
        self.storage.delete_post(post_id)
        return self.presenter.post_deleted()
        
        
