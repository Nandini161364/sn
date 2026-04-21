from django.db.models import Count 
from social.models import Reaction, Post

class ReactionStorage:
    def is_valid_post(self, post_id):
        return Post.objects.filter(post_id=post_id).exists()
    
    def get_total_reaction_count(self):
        result = Reaction.objects.aggregate(count=Count('id'))

        return {'count': result['count']}
    
    def get_reaction_metrics(self, post_id):
        result = (
            Reaction.objects.filter(post_id=post_id)
            .values("reaction")
            .annotate(count=Count("id"))
        )
        reaction_counts = {item["reaction"]: item["count"] for item in result}

        return reaction_counts
