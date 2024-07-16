from datetime import datetime

from sqlmodel import Field, SQLModel

from app.utils.date_utils import datetime_now_utc


class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime_now_utc, nullable=False)
    updated_at: datetime = Field(default_factory=datetime_now_utc, nullable=False)


class BaseResponse(SQLModel):
    id: int
    created_at: datetime
    updated_at: datetime
