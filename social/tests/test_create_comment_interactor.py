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
def test_create_comment():
    user = UserFactory()
    post = PostFactory(posted_by=user)

    comment_dto = CreateCommentDTO(
        user_id=user.user_id,
        post_id=post.post_id,
        content="This is a comment.",
        parent_comment_id=None
    )

    interactor = CreateCommentInteractor(
        storage=CommentStorage(),
        presenter=CommentPresenter(),
    )

    response = interactor.create_comment(comment_dto)
    with pytest.raises(InvalidUserException):
        invalid_user_dto = CreateCommentDTO(
            user_id="invalid_user",
            post_id=post.post_id,
            content="This is a comment.",
            parent_comment_id=None
        )
        interactor.create_comment(invalid_user_dto)
    with pytest.raises(InvalidPostException):
        invalid_post_dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id="invalid_post",
            content="This is a comment.",
            parent_comment_id=None
        )
        interactor.create_comment(invalid_post_dto)
    with pytest.raises(InvalidCommentException):
        invalid_comment_dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id=post.post_id,
            content="",
            parent_comment_id=None
        )
        interactor.create_comment(invalid_comment_dto)

    assert response["message"] == "Comment created successfully"
    assert "comment_id" in response

    comment_id = response["comment_id"]
    comment = Comment.objects.get(commented_id=comment_id)
    assert comment.content == "This is a comment."