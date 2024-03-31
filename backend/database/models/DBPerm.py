from typing import Optional
from sqlmodel import SQLModel, Field


class DBPerm(SQLModel, table=True):
    __tablename__ = "permissions"

    name: Optional[str] = Field(default=None, primary_key=True)
    level: Optional[int] = Field(default=0)
    can_grant: Optional[bool] = Field(default=False)
