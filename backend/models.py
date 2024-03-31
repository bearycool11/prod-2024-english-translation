from pydantic import BaseModel, Field
from typing import Optional


class PingResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    reason: str


class AuthSignInPostResponse(BaseModel):
    token: str


class AuthSignInPostRequest(BaseModel):
    login: str = Field(max_length=50)
    password: str


class AuthRegisterPostRequest(BaseModel):
    login: str = Field(max_length=50)
    password: str
    name: str = Field(max_length=50)


class UserProfile(BaseModel):
    id: int
    name: str = Field(max_length=50)
    login: str = Field(max_length=50)
    is_admin: bool


class UserPublicProfile(BaseModel):
    id: int
    name: str = Field(max_length=50)


class UserRights(BaseModel):
    rights: list[str]

class AuthRegisterPostResponse(BaseModel):
    profile: UserProfile


class OrganizationCreatePostRequest(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=150)


class Organization(BaseModel):
    id: int
    name: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=150)


class OrganizationCreatePostResponse(BaseModel):
    organization: Organization


class OrganizationUser(BaseModel):
    user: UserPublicProfile
    rights: UserRights

class UserOrganizationsGetResponse(BaseModel):
    organizations: list[Organization]
