from dataclasses import dataclass
from typing import Optional

@dataclass
class CreatePostDTO:
    user_id: int
    content: str
    group_id: Optional[str] = None


@dataclass
class CreateCommentDTO:
    user_id: str
    post_id: Optional[str]
    content: str
    parent_comment_id: Optional[str] = None


@dataclass
class CreateReactToPostDTO:
    user_id: str
    post_id: str
    reaction_type: str


@dataclass
class CreateReactToCommentDTO:
    user_id: str
    comment_id: str
    reaction_type: str

@dataclass
class DeletePostDto:
    user_id: str
    post_id: str

@dataclass
class CreateGroupDTO:
    name: str
    member_ids: list[int]
    user_id: str

@dataclass
class AddMemberToGroupDTO:
    group_id: str
    user_id: str
    member_id: int

@dataclass
class RemoveMemberFromGroupDTO:
    group_id: str
    user_id: str
    member_id: int


@dataclass
class MakeMemberAsAdminDTO:
    group_id: str
    user_id: str
    member_id: int


@dataclass
class GetGroupFeedDTO:
    user_id: str
    group_id: str
    offset: int
    limit: int
