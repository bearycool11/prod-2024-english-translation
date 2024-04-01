import datetime
import enum
from typing import Optional

from sqlalchemy import Column, BigInteger, Table, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import SQLModel, Field, Relationship


class Status(enum.Enum):
    OPEN = "OPEN"
    WAITING = "WAITING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"


class SentStatus(enum.Enum):
    NOT_READY = "NOT_READY"
    TIME_NOT_ENTERED = "TIME_NOT_ENTERED"
    WAITING = "WAITING"
    SENT_OK = "SENT_OK"
    SENT_ERROR = "SENT_ERROR"


class DBUser(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    login: str = Field(max_length=50, unique=True)
    password: str = Field(max_length=32)
    name: str = Field(max_length=50)
    is_admin: bool = Field(default=False)

    organization_bindings: list["DBOrganizationUser"] = Relationship(back_populates="user",
                                                                     sa_relationship_kwargs={"lazy": "dynamic"})


class DBPost(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True, unique=True)
    organization_id: int = Field(foreign_key="organizations.id")
    created_by: int = Field(foreign_key="users.id")
    content: str
    revision_id: int = Field(default=1, primary_key=True)
    is_approved: Status = Field(default=Status.OPEN)
    comment: Optional[str]
    planned_time: Optional[datetime.datetime]
    sent_status: SentStatus = Field(default=SentStatus.NOT_READY)

    channels: list["DBChannel"] = Relationship(sa_relationship_kwargs={"secondary": "post_channel_bindings",
                                                                       "primaryjoin": "DBPost.id==post_channel_bindings.c.post_id",
                                                                       "secondaryjoin": "DBChannel.id==post_channel_bindings.c.channel_id",
                                                                       "backref": "posts",
                                                                       "lazy": "dynamic"})


class DBPermission(SQLModel, table=True):
    __tablename__ = "permissions"

    name: str = Field(primary_key=True)
    level: int
    can_grant: bool = Field(default=False)


class DBChannel(SQLModel, table=True):
    __tablename__ = "channels"

    id: int = Field(sa_column=Column(BigInteger, primary_key=True, unique=True))
    bot_id: int = Field(foreign_key="organization_bots.bot_id")
    name: str

    posts: list[DBPost] = Relationship(sa_relationship_kwargs={"secondary": "post_channel_bindings",
                                                               "primaryjoin": "DBChannel.id==post_channel_bindings.c.channel_id",
                                                               "secondaryjoin": "DBPost.id==post_channel_bindings.c.post_id",
                                                               "backref": "channels",
                                                               "lazy": "dynamic"})


class DBOrganizationUser(SQLModel, table=True):
    __tablename__ = "organization_users"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    organization_id: int = Field(foreign_key="organizations.id", primary_key=True)
    permission: str = Field(foreign_key="permissions.name", primary_key=True)

    user: DBUser = Relationship(back_populates="organization_bindings")
    permission_data: DBPermission = Relationship()
    organization: "DBOrganization" = Relationship(back_populates="user_bindings")


class DBOrganization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=150)

    user_bindings: DBOrganizationUser = Relationship(back_populates="organization")


class DBOrganizationBot(SQLModel, table=True):
    __tablename__ = "organization_bots"

    organization_id: int = Field(foreign_key="organizations.id")
    bot_id: int = Field(primary_key=True)
    bot_token: str


class DBTask(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    handler: str
    arguments: dict = Field(default_factory=dict, sa_column=Column(JSON))
    planned_time: datetime.datetime


post_channel_bindings = Table(
    "post_channel_bindings",
    SQLModel.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("channel_id", Integer, ForeignKey("channels.id"), primary_key=True),
    UniqueConstraint('post_id', 'channel_id', name='_post_channel_bindings_uc'),
)
