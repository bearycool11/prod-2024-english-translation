from pydantic import BaseModel, Field


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
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    login: str = Field(max_length=50)
    is_admin: bool = Field(default=False)


class AuthRegisterPostResponse(BaseModel):
    profile: UserProfile
