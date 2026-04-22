import pytest

from social.exceptions import InvalidCommentException, InvalidPostException, InvalidUserException
from social.interactors.comments.create_comment_interactor import CreateCommentInteractor
from social.presenters.comment_presenter import CommentPresenter
from social.storages.comment_storage import CommentStorage
from social.tests.factories import UserFactory, GroupFactory, PostFactory, CommentFactory
from social.interactors.dtos import CreateCommentDTO

@pytest.mark.django_db
def test_reply_to_comment_interactor():
    user = UserFactory()
    post = PostFactory(posted_by=user)
    parent_comment = CommentFactory(post=post, commented_by=user)

    comment_dto = CreateCommentDTO(
        user_id=user.user_id,
        post_id=post.post_id,
        content="This is a reply to the comment.",
        parent_comment_id=parent_comment.commented_id
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
            content="This is a reply to the comment.",
            parent_comment_id=parent_comment.commented_id
        )
        interactor.create_comment(invalid_user_dto)
    with pytest.raises(InvalidPostException):
        invalid_post_dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id="invalid_post",
            content="This is a reply to the comment.",
            parent_comment_id=parent_comment.commented_id
        )
        interactor.create_comment(invalid_post_dto)
    with pytest.raises(InvalidCommentException):
        invalid_comment_dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id=post.post_id,
            content="",
            parent_comment_id=parent_comment.commented_id
        )
        interactor.create_comment(invalid_comment_dto)
    with pytest.raises(InvalidCommentException):
        invalid_parent_comment_dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id=post.post_id,
            content="This is a reply to the comment.",
            parent_comment_id=9999  
        )
        interactor.create_comment(invalid_parent_comment_dto)
    with pytest.raises(InvalidCommentException):
        invalid_parent_comment_dto = CreateCommentDTO(
            user_id=user.user_id,
            post_id=post.post_id,
            content="This is a reply to the comment.",
            parent_comment_id="invalid_parent_comment"  
        )
        interactor.create_comment(invalid_parent_comment_dto)

    assert response["message"] == "Comment created successfully"
    assert "comment_id" in response