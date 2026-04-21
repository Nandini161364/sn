class GetReactionsCountInteractor:
    def __init__(self, storage):
        self.storage = storage

    def get_total_reaction_count(self):
        return self.storage.get_total_reaction_count()
