from sqlmodel import Field, SQLModel


class DBUser(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    login: str = Field(max_length=50, unique=True)
    password: str = Field(max_length=32)
    name: str = Field(max_length=50)
    is_admin: bool = Field(default=False)
