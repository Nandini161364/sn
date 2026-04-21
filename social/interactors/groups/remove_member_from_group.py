from social.exceptions import (
    InvalidGroupException,
    InvalidMemberException,
    InvalidUserException,
    UserNotAdminException,
    UserNotInGroupException,
)


class RemoveMemberFromGroupInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
    
    def is_valid_user(self, user_id):
        return self.storage.is_valid_user(user_id)
    def is_valid_group(self, group_id):
        return self.storage.is_valid_group(group_id)
    def is_valid_member(self, member_id):
        return self.storage.is_valid_member(member_id)
    def is_user_admin(self, group_id, user_id):
        return self.storage.is_user_admin(group_id, user_id)
    def is_user_in_group(self, group_id, user_id):
        return self.storage.is_user_in_group(group_id, user_id)

    def remove_member_from_group(self, remove_member_from_group_dto):
        group_id = remove_member_from_group_dto.group_id
        user_id = remove_member_from_group_dto.user_id
        member_id = remove_member_from_group_dto.member_id

        if not self.storage.is_valid_group(group_id):
            raise InvalidGroupException("Invalid group")

        if not self.storage.is_valid_user(user_id):
            raise InvalidUserException("Invalid user")

        if not self.storage.is_valid_member(member_id):
            raise InvalidMemberException("Invalid member")

        if not self.storage.is_user_in_group(group_id, user_id):
            raise UserNotInGroupException("User not in group")

        if not self.storage.is_user_in_group(group_id, member_id):
            raise UserNotInGroupException("Member not in group")

        if not self.storage.is_user_admin(group_id, user_id):
            raise UserNotAdminException("User is not admin")

        self.storage.remove_member_from_group(remove_member_from_group_dto)
        return self.presenter.member_removed_successfully()
        
