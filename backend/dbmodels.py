from typing import Optional

from pydantic import types
from sqlalchemy import event, UniqueConstraint, Table, Column, Integer, ForeignKey, DateTime, func, UUID
from sqlmodel import Field, SQLModel, Relationship

class DBOrganization(SQLModel, table=True):
    __tablename__ = "orgs"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, max_length=50)
    image: str
    description: str

class DBUser(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    login: types.StringConstraints(max_length=50)
    email: types.StringConstraints(max_length=50)
    password: types.StringConstraints(max_length=32)
    is_admin: bool
