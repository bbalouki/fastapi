from datetime import datetime, timezone
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]


    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post  # Ensure all post data is inside a "post" key
    Votes: int

    class Config:
        from_attributes = True

