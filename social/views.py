from rest_framework.decorators import api_view
from rest_framework.response import Response

from .interactors.create_comment_interactor import CreateCommentInteractor
from .interactors.create_post_interactor import CreatePostInteractor
from .interactors.dtos import CreateCommentDTO, CreatePostDTO
from .presenters.comment_presenter import CommentPresenter
from .storages.post_storage import PostStorage
from .storages.comment_storage import CommentStorage
from .presenters.post_presenter import PostPresenter


@api_view(['POST'])
def create_post(request):

    content = request.data.get('content')
    user_id = request.data.get('user_id')

    post_dto = CreatePostDTO(
        user_id=user_id,
        content=content
    )

    storage = PostStorage()
    presenter = PostPresenter()

    interactor = CreatePostInteractor(storage=storage, presenter=presenter)

    response = interactor.create_post(post_dto)

    return Response(response)


@api_view(["POST"])
def create_comment(request):
    comment_dto = CreateCommentDTO(
        user_id=request.data.get("user_id"),
        post_id=request.data.get("post_id"),
        content=request.data.get("content"),
    )

    interactor = CreateCommentInteractor(
        storage=CommentStorage(),
        presenter=CommentPresenter(),
    )
    response = interactor.create_comment(comment_dto)
    return Response(response)
