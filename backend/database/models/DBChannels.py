from typing import Optional
from sqlmodel import SQLModel, Field


class DBChannels(SQLModel, table=True):
    __tablename__ = "channels"

    id: int = Field(primary_key=True)
    bot_id: int = Field(foreign_key="organization_bots.bot_id")
    name: str
    image: str
