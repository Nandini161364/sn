class AddMemberToGroupInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
    def add_member_to_group(self, add_member_dto):
        group_id = add_member_dto.group_id
        user_id = add_member_dto.user_id
        member_id = add_member_dto.member_id

        if not self.storage.is_valid_group(group_id):
            return self.presenter.invalid_group()
        
        if not self.storage.is_valid_user(user_id):
            return self.presenter.invalid_user(user_id)
        
        if not self.storage.is_user_admin(group_id, user_id):
            return self.presenter.not_admin()
        
        if not self.storage.is_valid_member(member_id):
            return self.presenter.invalid_member()
        
        if self.storage.is_new_user_already_member(group_id, member_id):
            return self.presenter.already_member()
        
        self.storage.add_member_to_group(add_member_dto)
        return self.presenter.member_added_successfully()