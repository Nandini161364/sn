from social.exceptions import (
    InvalidGroupException,
    InvalidMemberException,
    InvalidUserException,
    UserNotAdminException,
    UserNotInGroupException,
)


class MakeMemberAsAdminInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def make_member_as_admin(self, make_member_admin_dto):
        group_id = make_member_admin_dto.group_id
        user_id = make_member_admin_dto.user_id
        member_id = make_member_admin_dto.member_id

        if not self.storage.is_valid_user(user_id):
            raise InvalidUserException("Invalid user")

        if not self.storage.is_valid_member(member_id):
            raise InvalidMemberException("Invalid member")

        if not self.storage.is_valid_group(group_id):
            raise InvalidGroupException("Invalid group")

        if not self.storage.is_user_in_group(group_id, user_id):
            raise UserNotInGroupException("User not in group")

        if not self.storage.is_user_in_group(group_id, member_id):
            raise UserNotInGroupException("Member not in group")

        if not self.storage.is_user_admin(group_id, user_id):
            raise UserNotAdminException("User is not admin")

        self.storage.make_member_as_admin(make_member_admin_dto)
        return self.presenter.member_made_admin_successfully()
