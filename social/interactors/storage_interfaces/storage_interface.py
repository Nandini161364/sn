class PostStorageInterface:
    def is_valid_post(self, post_id):
            pass

    def is_valid_user(self, user_id):
        pass

    def is_valid_group(self, group_id):
        pass

    def is_user_in_group(self, group_id, user_id):
        pass

    def is_valid_reaction_type(self, reaction_type):
        pass

    def create_post(self, post_dto):
        pass
    
    def create_reaction(self, reaction_dto):
        pass

    def get_existing_reaction(self, reaction_dto):
        pass
    
    def delete_reaction(self, reaction_id):
        pass

    def update_reaction(self, reaction_id, reaction_type):
        pass
        

    def delete_post(self, post_id):
        pass
    
    def does_user_have_permission_to_delete_post(self, deletePostDto):
        pass

    def get_posts_with_more_positive_reactions(self):
        pass



    def get_posts_reacted_by_user(self, user_id):
        pass

    def get_reactions_to_post(self, post_id):
        pass

    def get_post(self, post_id):
        pass

    def get_user_posts(self, user_id):
        pass

    def get_group_feed(self, user_id, group_id, offset, limit):
        pass

    def get_posts_with_more_comments_than_reactions(self):
        pass
        
