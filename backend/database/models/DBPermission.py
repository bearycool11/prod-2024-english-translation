from sqlmodel import SQLModel, Field


class DBPermission(SQLModel, table=True):
    __tablename__ = "permissions"

    name: str = Field(primary_key=True)
    level: int
    can_grant: bool = Field(default=False)
