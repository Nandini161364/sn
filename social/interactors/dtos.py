from dataclasses import dataclass

@dataclass
class CreatePostDTO:
    user_id: int
    content: str


@dataclass
class CreateCommentDTO:
    user_id: str
    post_id: str
    content: str