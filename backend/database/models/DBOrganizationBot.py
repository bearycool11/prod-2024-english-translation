from typing import Optional
from sqlmodel import SQLModel, Field


class DBOrganizationBot(SQLModel, table=True):
    __tablename__ = "organization_bots"

    organization_id: int = Field(foreign_key="organizations.id")
    bot_id: int = Field(primary_key=True)
    bot_token: str
