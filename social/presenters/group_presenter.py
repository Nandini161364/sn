class GroupPresenter:
    def success_response(self, group_id):
        return {
            "message": "Group created successfully",
            "group_id": group_id
        }
    def invalid_group_name(self):
        return {
            "error": "Group name cannot be empty."
        }
    def invalid_user(self, user_id):
        return {
            "error": f"User with id {user_id} does not exist."
        }
    def invalid_member(self):
        return {
            "error": "Provided member ids are invalid."
        }
    def not_admin(self):
        return {
            "error": "User does not have admin privileges for this group."
        }
    def already_member(self):
        return {
            "error": "The user is already a member of the group."
        }
    def member_added_successfully(self):
        return {
            "message": "Member added to group successfully."
        }
    def group_not_found(self):
        return {
            "error": "Group not found."
        }
    def user_not_found(self):
        return {
            "error": "User not found."
        }
    def member_not_found(self):
        return {
            "error": "Member not found."
        }
    def member_removed_successfully(self):
        return {
            "message": "Member removed from group successfully."
        }
    def member_made_admin_successfully(self):
        return {
            "message": "Member made admin successfully."
        }
    def invalid_offset(self):
        return {
            "error": "Invalid offset value."
        }
    def invalid_limit(self):
        return {
            "error": "Invalid limit value."
        }
