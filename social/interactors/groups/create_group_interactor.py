
from social.exceptions import InvalidGroupNameException, InvalidUserException, InvalidMemberException

class CreateGroupInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_group(self, group_dto):
        if not self.storage.is_valid_group_name(group_dto.name):
            raise InvalidGroupNameException("Group name cannot be empty.")
        
        if not self.storage.is_valid_user(group_dto.user_id):
            raise InvalidUserException(f"User with id {group_dto.user_id} does not exist.")
        
        if not self.storage.is_valid_member(group_dto.member_ids):
            raise InvalidMemberException("One or more member ids are invalid.")
        
        group = self.storage.create_group(group_dto)
        return self.presenter.success_response(group.id)