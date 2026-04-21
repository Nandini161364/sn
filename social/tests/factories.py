import factory
from django.utils import timezone
from social.models import User, Group, Post, Comment, Reaction

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    user_id = factory.Faker("uuid4")
    name = factory.Faker("name")
    profile_pic = factory.Faker("image_url")


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker("sentence", nb_words=3)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    post_id = factory.Faker("uuid4")
    content = factory.Faker("text", max_nb_chars=100)
    posted_at = factory.LazyFunction(timezone.now)
    posted_by = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    commented_id = factory.Faker("uuid4")
    content = factory.Faker("text", max_nb_chars=100)
    commented_at = factory.LazyFunction(timezone.now)
    commented_by = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    parent_comment = None