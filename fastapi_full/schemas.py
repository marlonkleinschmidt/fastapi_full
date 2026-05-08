from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    username: str
    email: str
    id: int


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
