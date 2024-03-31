from typing import Optional

from sqlmodel import Field, SQLModel


class DBUser(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    login: str = Field(max_length=50)
    password: str = Field(max_length=32)
    is_admin: bool = Field(default=False)
