from social.exceptions import InvalidUserException, InvalidCommentException, InvalidReactionTypeException


class CreateReactToCommentInteractor:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter

    def create_reaction(self, reaction_dto):
        if not self.storage.is_valid_user(reaction_dto.user_id):
            raise InvalidUserException("Invalid user")

        if not self.storage.is_valid_comment(reaction_dto.comment_id):
            raise InvalidCommentException("Invalid comment")

        if not self.storage.is_valid_reaction_type(reaction_dto.reaction_type):
            raise InvalidReactionTypeException("Invalid reaction type")

        existing_reaction = self.storage.get_existing_reaction(reaction_dto)

        if existing_reaction:
            if existing_reaction['reaction'] == reaction_dto.reaction_type:
                self.storage.delete_reaction(existing_reaction['reaction_id'])
                return self.presenter.reaction_deleted()
            else:
                self.storage.update_reaction(existing_reaction['reaction_id'], reaction_dto.reaction_type)
                return self.presenter.reaction_updated()
        else:
            self.storage.create_reaction(reaction_dto)
            return self.presenter.reaction_created()
