import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import SQLModel, Field


class DBTask(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    handler: str
    arguments: dict = Field(default_factory=dict, sa_column=Column(JSON))
    planned_time: datetime.datetime
    next_run_delta: int = Field(default=-1)
