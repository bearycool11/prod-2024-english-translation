from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint


class DBOrgUser(SQLModel, table=True):
    __tablename__ = "organization_users"

    user_id: Optional[int] = Field(foreign_key="users.id", primary_key=True)
    organization_id: Optional[int] = Field(foreign_key="organizations.id", primary_key=True)
    permission: Optional[str] = Field(foreign_key="permissions.name", primary_key=True)

    __table_args__ = UniqueConstraint("user_id", "organization_id", "permission", name="_organization_users_uc"),

