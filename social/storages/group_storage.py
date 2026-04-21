from social.models import Group, Membership, User

# create_group should return the id of the newly created group.
# It should raise InvalidUserException if the given user_id is not in the database.
# It should also raise InvalidGroupNameException if the given name is empty.
# It should also raise InvalidMemberException if any of the given member_ids is not in the database.
# Ignore any duplicates in member_ids and add them only once.
# Make sure user_id is set as admin for the newly created group.



class GroupStorage:
    def is_valid_user(self, user_id):
        return User.objects.filter(user_id=user_id).exists()
    
    def is_valid_group_name(self, name):
        return bool(name and name.strip())
    
    def is_valid_member(self, member_ids):
        if isinstance(member_ids, (list, tuple, set)):
            return all(self.is_valid_user(member_id) for member_id in member_ids)
        return User.objects.filter(user_id=member_ids).exists()
    
    def create_group(self, group_dto):
        user = User.objects.get(user_id=group_dto.user_id)
        group = Group.objects.create(name=group_dto.name)

        unique_member_ids = set(group_dto.member_ids)
        unique_member_ids.discard(group_dto.user_id)

        members = [User.objects.get(user_id=member_id) for member_id in unique_member_ids]
        group.members.set(members)

        Membership.objects.create(user=user, group=group, is_admin=True)

        return group
    
    def is_valid_group(self, group_id):
        return Group.objects.filter(id=group_id).exists()
    
    def is_user_admin(self, group_id, user_id):
        return Membership.objects.filter(group_id=group_id, user__user_id=user_id, is_admin=True).exists()
    
    def is_new_user_already_member(self, group_id, member_id):
        return Membership.objects.filter(group_id=group_id, user__user_id=member_id).exists()
    
    def is_user_in_group(self, group_id, user_id):
        return Membership.objects.filter(group_id=group_id, user__user_id=user_id).exists()
        
    def add_member_to_group(self, add_member_dto):
        group = Group.objects.get(id=add_member_dto.group_id)
        new_member = User.objects.get(user_id=add_member_dto.member_id)

        Membership.objects.create(group=group, user=new_member, is_admin=False)
        return
    def remove_member_from_group(self, remove_member_dto):
        Membership.objects.filter(group_id=remove_member_dto.group_id, user__user_id=remove_member_dto.member_id).delete()
        return
    
    def make_member_as_admin(self, make_member_admin_dto):
        membership = Membership.objects.get(
            group_id=make_member_admin_dto.group_id,
            user__user_id=make_member_admin_dto.member_id,
        )
        if membership.is_admin:
            return

        membership.is_admin = True
        membership.save(update_fields=["is_admin"])

    def get_silent_group_members(self, group_id):
        member_ids_with_posts = set(
            Group.objects.get(id=group_id)
            .posts.values_list("posted_by_id", flat=True)
            .distinct()
        )
        return list(
            Membership.objects.filter(group_id=group_id)
            .exclude(user__user_id__in=member_ids_with_posts)
            .values_list("user__user_id", flat=True)
        )
        
        

        

    # def get_group_by_id(self, group_id):
    #     try:
    #         return Group.objects.get(id=group_id)
    #     except Group.DoesNotExist:
    #         return None

    # def add_member(self, group, user, is_admin=False):
    #     membership, created = Membership.objects.get_or_create(group=group, user=user)
    #     if not created:
    #         return membership
    #     membership.is_admin = is_admin
    #     membership.save()
    #     return membership

    # def remove_member(self, group, user):
    #     Membership.objects.filter(group=group, user=user).delete()

    # def list_members(self, group):
    #     return group.members.all()
