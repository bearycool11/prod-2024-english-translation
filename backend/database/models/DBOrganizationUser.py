from typing import Optional
from sqlmodel import SQLModel, Field


class DBOrganizationUser(SQLModel, table=True):
    __tablename__ = "organization_users"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    organization_id: int = Field(foreign_key="organizations.id", primary_key=True)
    permission: str = Field(foreign_key="permissions.name", primary_key=True)
