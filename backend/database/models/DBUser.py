from typing import Optional

from sqlmodel import Field, SQLModel


class DBUser(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    login: Optional[str] = Field(max_length=50)
    email: Optional[str] = Field(max_length=50)
    password: Optional[str] = Field(max_length=32)
    is_admin: Optional[bool]
