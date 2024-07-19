from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base_models import Base, BaseResponse


class PostBase(SQLModel):
    title: str = Field(min_length=4, max_length=64, unique=True, nullable=False)
    content: str | None = Field(default=None, nullable=True)


class Post(Base, PostBase, table=True):
    user_id: int = Field(foreign_key="user.id", nullable=False)
    archived_at: datetime | None = Field(default=None, nullable=True)


class PostRequest(PostBase):
    pass


class PostResponse(BaseResponse, PostBase):
    user_id: int
    archived_at: datetime | None
