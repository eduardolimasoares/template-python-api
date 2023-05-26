from pydantic import BaseModel as SCBaseModel
from datetime import datetime
from typing import Optional


class UserSchema(SCBaseModel):
    id:             Optional[int]
    name:           Optional[str]
    email:          str
    status:         Optional[int]

    class Config:
        orm_mode = True

class UserSchemaRequest(UserSchema):
    password:       str


class UserStatusSchema(SCBaseModel):
    id:             int
    status:         str

    class Config:
        orm_mode = True

class UserForgotTokeSchema(SCBaseModel):
    user_id:        int
    token:          str
    expiredat:      datetime

    class Config:
        orm_mode = True

class UserSchemaUpdate(UserSchema):
    id:             Optional[int]
    name:           Optional[str]
    password:       Optional[str]
    email:          Optional[str]
    status:         Optional[int]


class RecoverPassSchema(SCBaseModel):
    email:          str

    class Config:
        orm_mode = True