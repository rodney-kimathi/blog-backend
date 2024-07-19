from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base_models import Base, BaseResponse


class PostBase(SQLModel):
    title: str = Field(min_length=4, max_length=64, unique=True, nullable=False)
    content: str | None = Field(default=None, nullable=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)


class PostDetailBase(SQLModel):
    post_id: int = Field(foreign_key="post.id", nullable=False)
    content: str | None = Field(default=None, nullable=True)


class Post(Base, PostBase, table=True):
    archived_at: datetime | None = Field(default=None, nullable=True)


class PostDetail(Base, PostDetailBase, table=True):
    pass


class PostRequest(PostBase):
    pass


class PostResponse(BaseResponse, PostBase):
    archived_at: datetime | None
