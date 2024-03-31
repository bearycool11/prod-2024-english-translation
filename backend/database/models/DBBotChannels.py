from typing import Optional
from sqlmodel import SQLModel, Field


class DBBotChannels(SQLModel, table=True):
    __tablename__ = "bot_channels"

    bot_id: int = Field(foreign_key="organization_bots.bot_id")
    channel_id: int = Field(primary_key=True)
    name: str
    image: str
