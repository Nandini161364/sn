class GetPostsWithMoreCommentsThanReactionsInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_posts_with_more_comments_than_reactions(self):
        return self.storage.get_posts_with_more_comments_than_reactions()
