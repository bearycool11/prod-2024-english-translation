from typing import Optional

from sqlmodel import SQLModel, Field


class DBOrganization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, unique=True, max_length=50)
    description: Optional[str] = Field(default=None, unique=True, max_length=150)
