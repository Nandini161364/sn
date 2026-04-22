
import pytest
from social.interactors.posts.create_post_interactor import CreatePostInteractor
from social.exceptions import (
    InvalidGroupException,
    InvalidPostException,
    InvalidUserException,
    UserNotInGroupException,
)
from social.models import User, Post, Group, Membership
from social.tests.factories import UserFactory, GroupFactory
from social.interactors.posts.create_post_interactor import CreatePostInteractor
from social.interactors.dtos import CreatePostDTO
from social.storages.post_storage import PostStorage
from social.presenters.post_presenter import PostPresenter

@pytest.mark.django_db
def test_create_post_with_group():
    user = UserFactory()
    group = GroupFactory()
    group.members.add(user)

    dto = CreatePostDTO(
        user_id=user.user_id,
        content="Hello world",
        group_id=group.id,
    )

    interactor = CreatePostInteractor(
        storage=PostStorage(),
        presenter=PostPresenter(),
    )

    response = interactor.create_post(dto)

    with pytest.raises(InvalidGroupException):
        invalid_group_dto = CreatePostDTO(
            user_id=user.user_id,
            content="Hello world",
            group_id=9999,  
        )
        interactor.create_post(invalid_group_dto)
    with pytest.raises(InvalidUserException):
        invalid_user_dto = CreatePostDTO(
            user_id="invalid_user",
            content="Hello world",
            group_id=group.id,
        )
        interactor.create_post(invalid_user_dto)
    with pytest.raises(UserNotInGroupException):
        other_user = UserFactory()
        user_not_in_group_dto = CreatePostDTO(
            user_id=other_user.user_id,
            content="Hello world",
            group_id=group.id,
        )
        interactor.create_post(user_not_in_group_dto)
    with pytest.raises(InvalidPostException):
        invalid_post_dto = CreatePostDTO(
            user_id=user.user_id,
            content="",
            group_id=group.id,
        )
        interactor.create_post(invalid_post_dto)

    assert response["message"] == "Post created successfully"
    assert "post_id" in response
    assert Post.objects.filter(post_id=response["post_id"], posted_by=user, group=group).exists()