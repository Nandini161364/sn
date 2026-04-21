import pytest
from social.models import User, Post

# @pytest.mark.django_db
# def test_create_user():
#     user = User.objects.create(user_id="user_1", name="John Doe", profile_pic="test")
#     assert user.user_id == "user_1"
#     assert user.name == "John Doe"
#     assert user.profile_pic == "test"


# @pytest.mark.django_db
# def test_create_post():
#     user = User.objects.create(user_id="user_1", name="John Doe", profile_pic="test")
#     post = Post.objects.create(post_id="post_1", content="Hello World", posted_by=user)
#     assert post.post_id == "post_1"
#     assert post.content == "Hello World"
#     assert post.posted_by == user