from social.exceptions import InvalidGroupException


class GetSilentGroupMembersInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_silent_group_members(self, group_id):
        if not self.storage.is_valid_group(group_id):
            raise InvalidGroupException("Invalid group")

        return self.storage.get_silent_group_members(group_id)
