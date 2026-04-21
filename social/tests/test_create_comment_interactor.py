import pytest
from social.exceptions import (
    InvalidUserException,
    InvalidPostException,
    InvalidCommentException,
)
from social.models import Comment
from social.interactors.comments.create_comment_interactor import CreateCommentInteractor
from social.interactors.dtos import CreateCommentDTO
from social.storages.comment_storage import CommentStorage
from social.presenters.comment_presenter import CommentPresenter
from social.tests.factories import UserFactory, PostFactory


@pytest.mark.django_db
def test_create_comment_interactor():
    user = UserFactory()
    post = PostFactory(posted_by=user)
    
    dto = CreateCommentDTO(
        user_id=user.user_id,
        post_id=post.post_id,
        content="Hello world",
    )

    interactor = CreateCommentInteractor(
        storage=CommentStorage(),
        presenter=CommentPresenter(),
    )

    response = interactor.create_comment(dto)

    with pytest.raises(InvalidUserException):
        dto = CreateCommentDTO(
            user_id="invalid_user",
            post_id=post.post_id,
            content="Hello world",
        )
        interactor.create_comment(dto)

    with pytest.raises(InvalidPostException):
        dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id="invalid_post",
            content="Hello world",
        )
        interactor.create_comment(dto)

    with pytest.raises(InvalidCommentException):
        dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id=post.post_id,
            content="",
        )
        interactor.create_comment(dto)
    
    assert response["message"] == "Comment created successfully"
    assert "comment_id" in response
    assert Comment.objects.filter(commented_id=response["comment_id"], content="Hello world").exists()
