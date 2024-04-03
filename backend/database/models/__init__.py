import datetime
import enum
from typing import Optional

from sqlalchemy import Column, BigInteger, Table, ForeignKey, Integer, UniqueConstraint, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import SQLModel, Field, Relationship


class Status(enum.Enum):
    OPEN = "OPEN"
    WAITING = "WAITING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"


class SentStatus(enum.Enum):
    NOT_READY = "NOT_READY"
    TIME_NOT_ENTERED = "TIME_NOT_ENTERED"  # not using this one
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
    posts: list["DBPost"] = Relationship(back_populates="user")


class DBPost(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(default=None, primary_key=True, unique=True)
    organization_id: int = Field(foreign_key="organizations.id")
    created_by: int = Field(foreign_key="users.id")
    content: str
    is_approved: Status = Field(default=Status.OPEN)
    comment: Optional[str]
    planned_time: Optional[datetime.datetime]
    sent_status: SentStatus = Field(default=SentStatus.NOT_READY)
    updated_at: datetime.datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now()))

    user: DBUser = Relationship(back_populates="posts")
    tag_bindings: list["DBTag"] = Relationship(back_populates="post", sa_relationship_kwargs={"lazy": "dynamic"})
    channels: list["DBChannel"] = Relationship(sa_relationship_kwargs={"secondary": "post_channel_bindings",
                                                                       "primaryjoin": "DBPost.id==post_channel_bindings.c.post_id",
                                                                       "secondaryjoin": "DBChannel.id==post_channel_bindings.c.channel_id",
                                                                       "back_populates": "posts",
                                                                       "lazy": "dynamic"})
    organization: "DBOrganization" = Relationship()
    sent_infos: list["DBSentPostInfo"] = Relationship(back_populates="post")


class DBPermission(SQLModel, table=True):
    __tablename__ = "permissions"

    name: str = Field(primary_key=True)
    level: int
    can_grant: bool = Field(default=False)


class DBChannel(SQLModel, table=True):
    __tablename__ = "channels"

    id: int = Field(primary_key=True, default=None, unique=True)
    telegram_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    bot_id: int = Field(foreign_key="organization_bots.bot_id")
    name: str

    posts: list[DBPost] = Relationship(sa_relationship_kwargs={"secondary": "post_channel_bindings",
                                                               "primaryjoin": "DBChannel.id==post_channel_bindings.c.channel_id",
                                                               "secondaryjoin": "DBPost.id==post_channel_bindings.c.post_id",
                                                               "back_populates": "channels",
                                                               "lazy": "dynamic"})
    bot: "DBOrganizationBot" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "DBOrganizationBot.bot_id==DBChannel.bot_id"})
    sent_infos: list["DBSentPostInfo"] = Relationship()


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
    bots: list["DBOrganizationBot"] = Relationship(back_populates="organization", sa_relationship_kwargs={
        "primaryjoin": "DBOrganizationBot.organization_id==DBOrganization.id"
    })


class DBOrganizationBot(SQLModel, table=True):
    __tablename__ = "organization_bots"

    organization_id: int = Field(foreign_key="organizations.id")
    bot_id: int = Field(primary_key=True)
    bot_token: str

    organization: DBOrganization = Relationship(back_populates="bots")


class DBTask(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    handler: str
    arguments: dict = Field(default_factory=dict, sa_column=Column(JSON))
    planned_time: datetime.datetime
    next_run_delta: int = Field(default=-1)


class DBTag(SQLModel, table=True):
    tag: str = Field(primary_key=True)
    post_id: int = Field(foreign_key="posts.id", primary_key=True)

    post: DBPost = Relationship(back_populates="tag_bindings")


class DBSentPostInfo(SQLModel, table=True):
    __tablename__ = "sent_post_info"

    id: int = Field(primary_key=True, default=None, unique=True)
    post_id: Optional[int] = Field(foreign_key="posts.id", nullable=True)
    channel_id: Optional[int] = Field(foreign_key="channels.id", nullable=True)
    telegram_message_id: Optional[int] = Field(sa_column=Column(BigInteger, nullable=True))
    chat_username: Optional[str] = Field(nullable=True)

    post: DBPost = Relationship(back_populates="sent_infos")
    channel: DBChannel = Relationship(back_populates="sent_infos")


class DBOrganizationStopToggle(SQLModel, table=True):
    __tablename__ = "organization_stop_toggles"

    organization_id: int = Field(primary_key=True, default=None)


post_channel_bindings = Table(
    "post_channel_bindings",
    SQLModel.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("channel_id", Integer, ForeignKey("channels.id"), primary_key=True),
    UniqueConstraint('post_id', 'channel_id', name='_post_channel_bindings_uc'),
)
