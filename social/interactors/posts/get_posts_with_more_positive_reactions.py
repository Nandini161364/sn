class GetPostsWithMorePositiveReactionsInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_posts_with_more_positive_reactions(self):
        return self.storage.get_posts_with_more_positive_reactions()
