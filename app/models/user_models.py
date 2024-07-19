from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.models.base_models import Base, BaseResponse


class UserBase(SQLModel):
    username: str = Field(min_length=4, max_length=16, unique=True, nullable=False)
    password: str = Field(min_length=8, max_length=64, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    full_name: str = Field(min_length=6, max_length=32, nullable=False)


class User(Base, UserBase, table=True):
    active: bool = Field(default=True, nullable=False)


class UserRequest(UserBase):
    pass


class UserResponse(BaseResponse, UserBase):
    active: bool
    password: str = Field(exclude=True)
