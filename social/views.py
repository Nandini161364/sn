from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from social.presenters.group_presenter import GroupPresenter
from social.storages.group_storage import GroupStorage

from .interactors.comments import (
    CreateCommentInteractor,
    GetRepliesForCommentInteractor,
    CreateReactToCommentInteractor,
)
from .interactors.posts import (
    CreatePostInteractor,
    CreateReactToPostInteractor,
    DeletePostInteractor,
    GetPostInteractor,
    GetPostsReactedByUserInteractor,
    GetPostsWithMoreCommentsThanReactionsInteractor,
    GetPostsWithMorePositiveReactionsInteractor,
    GetReactionsToPostInteractor,
    GetUserPostsInteractor,
)
from .interactors.reactions import (
    GetReactionMetricsInteractor,
    GetReactionsCountInteractor,
)

from .interactors.groups import (
    AddMemberToGroupInteractor,
    CreateGroupInteractor,
    GetGroupFeedInteractor,
    GetSilentGroupMembersInteractor,
    MakeMemberAsAdminInteractor,
    RemoveMemberFromGroupInteractor,
)

from .interactors.dtos import (
    CreateCommentDTO, 
    CreatePostDTO, 
    CreateReactToPostDTO, 
    CreateReactToCommentDTO, 
    DeletePostDto,
    CreateGroupDTO,
    AddMemberToGroupDTO,
    GetGroupFeedDTO,
    MakeMemberAsAdminDTO,
    RemoveMemberFromGroupDTO,
)

from .presenters.comment_presenter import CommentPresenter
from .presenters.reaction_presenter import ReactionPresenter
from .presenters.post_presenter import PostPresenter

from .storages.post_storage import PostStorage
from .storages.comment_storage import CommentStorage
from .storages.reactions_storage import ReactionStorage



from .exceptions import (
    InvalidGroupNameException, 
    InvalidMemberException, 
    InvalidUserException, 
    InvalidPostException, 
    InvalidCommentException, 
    InvalidReactionTypeException,
    UserCannotDeletePostException,
    InvalidGroupException,
    InvalidLimitSetValueException,
    InvalidOffSetValueException,
    UserNotInGroupException,
    UserNotAdminException
)


@api_view(['POST'])
def create_post(request):
    try:
        content = request.data.get('content') or request.data.get("post_content")
        user_id = request.data.get('user_id')
        group_id = request.data.get("group_id")

        post_dto = CreatePostDTO(
            user_id=user_id,
            content=content,
            group_id=group_id,
        )

        storage = PostStorage()
        presenter = PostPresenter()

        interactor = CreatePostInteractor(storage=storage, presenter=presenter)

        response = interactor.create_post(post_dto)

        return Response(response)
    except InvalidUserException:
        return Response(PostPresenter().invalid_user(), status=400)
    except InvalidPostException:
        return Response(PostPresenter().invalid_post(), status=400)
    except InvalidGroupException:
        return Response(GroupPresenter().group_not_found(), status=400)
    except UserNotInGroupException:
        return Response(GroupPresenter().user_not_found(), status=400)


@api_view(["POST"])
@api_view(['POST'])
def create_comment(request):
    try:
        comment_dto = CreateCommentDTO(
            user_id=request.data.get("user_id"),
            post_id=request.data.get("post_id"),
            content=request.data.get("content"),
            parent_comment_id=None,
        )

        interactor = CreateCommentInteractor(
            storage=CommentStorage(),
            presenter=CommentPresenter(),
        )
        response = interactor.create_comment(comment_dto)
        return Response(response)
    except InvalidUserException:
        return Response(CommentPresenter().invalid_user(), status=400)
    except InvalidPostException:
        return Response(CommentPresenter().invalid_post(), status=400)
    except InvalidCommentException:
        return Response(CommentPresenter().invalid_comment_content(), status=400)


@api_view(["POST"])
def reply_to_comment(request):
    try:
        storage = CommentStorage()
        parent_comment_id = request.data.get("comment_id")
        post_id = storage.get_post_id_for_comment(parent_comment_id)

        if not post_id:
            return Response(CommentPresenter().invalid_parent_comment())

        reply_comment_dto = CreateCommentDTO(
            user_id=request.data.get("user_id"),
            post_id=post_id,
            content=request.data.get("reply_content"),
            parent_comment_id=parent_comment_id,
        )

        interactor = CreateCommentInteractor(
            storage=storage,
            presenter=CommentPresenter(),
        )
        response = interactor.create_comment(reply_comment_dto)
        return Response(response)
    except InvalidUserException:
        return Response(CommentPresenter().invalid_user(), status=400)
    except InvalidPostException:
        return Response(CommentPresenter().invalid_post(), status=400)
    except InvalidCommentException:
        return Response(CommentPresenter().invalid_comment_content(), status=400)


@api_view(["POST"])
def react_to_post(request):
    try:
        react_to_post_dto = CreateReactToPostDTO(
            user_id=request.data.get("user_id"),
            post_id=request.data.get("post_id"),
            reaction_type=request.data.get("reaction_type")
        )
        
        interactor = CreateReactToPostInteractor(
            storage=PostStorage(),
            presenter=ReactionPresenter(),
        )
        response = interactor.create_reaction(react_to_post_dto)
        return Response(response)
    
    except InvalidUserException:
        return Response(ReactionPresenter().invalid_user(), status=400)
    except InvalidPostException:
        return Response(ReactionPresenter().invalid_post(), status=400)
    except InvalidReactionTypeException:
        return Response(ReactionPresenter().invalid_reaction_type(), status=400)


@api_view(["POST"])
def react_to_comment(request):
    try:
        react_to_comment_dto = CreateReactToCommentDTO(
            user_id=request.data.get("user_id"),
            comment_id=request.data.get("comment_id"),
            reaction_type=request.data.get("reaction_type")
        )
        
        interactor = CreateReactToCommentInteractor(
            storage=CommentStorage(),
            presenter=ReactionPresenter(),
        )
        response = interactor.create_reaction(react_to_comment_dto)
        return Response(response)
    
    except InvalidUserException:
        return Response(ReactionPresenter().invalid_user(), status=400)
    except InvalidCommentException:
        return Response(ReactionPresenter().invalid_comment(), status=400)
    except InvalidReactionTypeException:
        return Response(ReactionPresenter().invalid_reaction_type(), status=400)


@api_view(['GET'])
def get_total_reactions(request):
    interactor = GetReactionsCountInteractor(
            storage=ReactionStorage(),
    )
    response = interactor.get_total_reaction_count()
    return Response(response)


@api_view(["GET"])
def get_reaction_metrics(request):
    try:
        post_id = request.query_params.get("post_id")

        interactor = GetReactionMetricsInteractor(
            storage=ReactionStorage()
        )
        response = interactor.get_reaction_metrics(post_id)

        return Response(response)

    except InvalidPostException:
        return Response(ReactionPresenter().invalid_post(), status=400)
    

@api_view(["DELETE"])
@authentication_classes([OAuth2Authentication])
@protected_resource(['superuser'])
def delete_post(request, post_id):
    try:
        delete_post_dto = DeletePostDto(
            user_id= request.data.get("user_id"),
            post_id= post_id
        )
        interactor = DeletePostInteractor(
            storage=PostStorage(),
            presenter=PostPresenter(),
        )
        response = interactor.delete_post(delete_post_dto)

        return Response(response)

    except InvalidUserException:
        return Response(PostPresenter().invalid_user(), status=400)
    except InvalidPostException:
        return Response(PostPresenter().invalid_post(), status=400)
    except UserCannotDeletePostException:
        return Response(PostPresenter().user_cannot_delete_post(), status=400)

@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@protected_resource(['superuser'])

def get_posts_with_more_positive_reactions(request):
    interactor = GetPostsWithMorePositiveReactionsInteractor(
            storage=PostStorage()
        )
    response = interactor.get_posts_with_more_positive_reactions()
    return Response(response)


@api_view(["GET"])
def get_posts_reacted_by_user(request):
    try:
        user_id = request.query_params.get("user_id")
        interactor = GetPostsReactedByUserInteractor(
            storage=PostStorage()
        )
        response = interactor.get_posts_reacted_by_user(user_id)
        return Response(response)
    except InvalidUserException:
        return Response(PostPresenter().invalid_user(), status=400)


@api_view(["GET"])
def get_reactions_to_post(request):
    try:
        post_id = request.query_params.get("post_id")
        interactor = GetReactionsToPostInteractor(
            storage=PostStorage(),
            presenter=PostPresenter()
        )
        response = interactor.get_reactions_to_post(post_id)
        return Response(response)
    except InvalidPostException:
        return Response(PostPresenter().invalid_post(), status=400)


@api_view(["GET"])
def get_post(request):
    try:
        post_id = request.query_params.get("post_id")
        interactor = GetPostInteractor(
            storage=PostStorage(),
            presenter=PostPresenter()
        )
        response = interactor.get_post(post_id)
        return Response(response)
    except InvalidPostException:
        return Response(PostPresenter().invalid_post(), status=400)


@api_view(["GET"])
def get_user_posts(request):
    try:
        user_id = request.query_params.get("user_id")
        interactor = GetUserPostsInteractor(
            storage=PostStorage(),
            presenter=PostPresenter()
        )
        response = interactor.get_user_posts(user_id)
        return Response(response)
    except InvalidUserException:
        return Response(PostPresenter().invalid_user(), status=400)


@api_view(["GET"])
def get_replies_for_comment(request):
    try:
        comment_id = request.query_params.get("comment_id")
        interactor = GetRepliesForCommentInteractor(
            storage=CommentStorage(),
            presenter=CommentPresenter()
        )
        response = interactor.get_replies_for_comment(comment_id)
        return Response(response)
    except InvalidCommentException:
        return Response(ReactionPresenter().invalid_comment(), status=400)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def create_group(request):
    try:
        group_dto = CreateGroupDTO(
            user_id=request.data.get("user_id"),
            name=request.data.get("name"),
            member_ids=request.data.get("member_ids", [])
        )

        interactor = CreateGroupInteractor(
            storage=GroupStorage(),
            presenter=GroupPresenter(),
        )
        response = interactor.create_group(group_dto)
        return Response(response)
    except InvalidGroupNameException:
        return Response(GroupPresenter().invalid_group_name(), status=400)
    except InvalidUserException as e:
        return Response(GroupPresenter().invalid_user(e.args[0]), status=400)
    except InvalidMemberException:
        return Response(GroupPresenter().invalid_member(), status=400)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def add_member_to_group(request):
    try:
        add_member_to_group_dto = AddMemberToGroupDTO(
            user_id=request.data.get("user_id"),
            group_id=request.data.get("group_id"),
            member_id=request.data.get("new_member_id")
        )

        interactor = AddMemberToGroupInteractor(
            storage=GroupStorage(),
            presenter=GroupPresenter(),
        )

        response = interactor.add_member_to_group(add_member_to_group_dto)
        return Response(response)
    except InvalidUserException as e:
        return Response(GroupPresenter().invalid_user(e.args[0] if e.args else request.data.get("user_id")), status=400)
    except InvalidGroupException:
        return Response(GroupPresenter().group_not_found(), status=400)
    except InvalidMemberException:
        return Response(GroupPresenter().invalid_member(), status=400)
    except UserNotAdminException:
        return Response(GroupPresenter().not_admin(), status=400)
    except UserNotInGroupException:
        return Response(GroupPresenter().user_not_found(), status=400)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def remove_member_from_group(request):
    try:
        remove_member_from_group_dto = RemoveMemberFromGroupDTO(
            user_id=request.data.get("user_id"),
            group_id=request.data.get("group_id"),
            member_id=request.data.get("member_id")
        )
        interactor = RemoveMemberFromGroupInteractor(
            storage=GroupStorage(),
            presenter=GroupPresenter(),
        )
        response = interactor.remove_member_from_group(remove_member_from_group_dto)
        return Response(response)
    except InvalidUserException as e:
        return Response(GroupPresenter().invalid_user(e.args[0] if e.args else request.data.get("user_id")), status=400)
    except InvalidGroupException:
        return Response(GroupPresenter().group_not_found(), status=400)
    except InvalidMemberException:
        return Response(GroupPresenter().invalid_member(), status=400)
    except UserNotAdminException:
        return Response(GroupPresenter().not_admin(), status=400)
    except UserNotInGroupException:
        return Response(GroupPresenter().user_not_found(), status=400)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def make_member_as_admin(request):
    try:
        make_member_as_admin_dto = MakeMemberAsAdminDTO(
            user_id=request.data.get("user_id"),
            group_id=request.data.get("group_id"),
            member_id=request.data.get("member_id"),
        )

        interactor = MakeMemberAsAdminInteractor(
            storage=GroupStorage(),
            presenter=GroupPresenter(),
        )
        response = interactor.make_member_as_admin(make_member_as_admin_dto)
        return Response(response)
    except InvalidUserException as e:
        return Response(GroupPresenter().invalid_user(e.args[0] if e.args else request.data.get("user_id")), status=400)
    except InvalidGroupException:
        return Response(GroupPresenter().group_not_found(), status=400)
    except InvalidMemberException:
        return Response(GroupPresenter().invalid_member(), status=400)
    except UserNotAdminException:
        return Response(GroupPresenter().not_admin(), status=400)
    except UserNotInGroupException:
        return Response(GroupPresenter().user_not_found(), status=400)


@api_view(["GET"])
def get_group_feed(request):
    try:
        group_feed_dto = GetGroupFeedDTO(
            user_id=request.query_params.get("user_id"),
            group_id=request.query_params.get("group_id"),
            offset=int(request.query_params.get("offset", 0)),
            limit=int(request.query_params.get("limit", 10)),
        )

        interactor = GetGroupFeedInteractor(
            storage=PostStorage(),
            presenter=PostPresenter()
        )
        response = interactor.get_group_feed(group_feed_dto)
        return Response(response)
    except ValueError:
        return Response(GroupPresenter().invalid_offset(), status=400)
    except InvalidUserException as e:
        return Response(GroupPresenter().invalid_user(e.args[0] if e.args else request.query_params.get("user_id")), status=400)
    except InvalidGroupException:
        return Response(GroupPresenter().group_not_found(), status=400)
    except UserNotInGroupException:
        return Response(GroupPresenter().user_not_found(), status=400)
    except InvalidOffSetValueException:
        return Response(GroupPresenter().invalid_offset(), status=400)
    except InvalidLimitSetValueException:
        return Response(GroupPresenter().invalid_limit(), status=400)


@api_view(["GET"])
def get_posts_with_more_comments_than_reactions(request):
    interactor = GetPostsWithMoreCommentsThanReactionsInteractor(
        storage=PostStorage()
    )
    response = interactor.get_posts_with_more_comments_than_reactions()
    return Response(response)


@api_view(["GET"])
def get_silent_group_members(request):
    try:
        group_id = request.query_params.get("group_id")
        interactor = GetSilentGroupMembersInteractor(storage=GroupStorage())
        response = interactor.get_silent_group_members(group_id)
        return Response(response)
    except InvalidGroupException:
        return Response(GroupPresenter().group_not_found(), status=400)
