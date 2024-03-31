from sqlmodel import SQLModel, Field
import enum

class Status(enum.Enum):
    OPEN = "OPEN"
    WAITING = "WAITING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"


class DBPost(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True)
    organization_id: int = Field(foreign_key="organizations.id")
    created_by: int = Field(foreign_key="users.id")
    content: str
    revision_id: int = Field(default=1)
    is_approved: Status = Field(default=Status.OPEN)
    comment: str

