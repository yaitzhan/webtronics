from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class UserAdditionalBase(BaseModel):
    full_name: Optional[str]
    time_zone: Optional[str]
    city: Optional[str]
    country: Optional[str]
    email_status: Optional[str]
    email_score: Optional[str]
    email_disposable: Optional[str]
    email_gibberish: Optional[str]


class UserAdditionalCreate(BaseModel):
    id: int


class UserAdditionalUpdate(UserAdditionalBase):
    pass


class UserAdditional(UserAdditionalBase):
    class Config:
        orm_mode = True
