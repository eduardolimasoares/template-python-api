from app.core.configs import settings
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class UserStatus(settings.DBBaseModel):
    __tablename__ = 'status'
    id:         int = Column(Integer, primary_key=True, autoincrement=True)
    status:     int = Column(String(50))

class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'
    id:         int = Column(Integer, primary_key=True, autoincrement=True)
    name:       str = Column(String(100))
    password:   str = Column(String(100))
    email:      str = Column(String(100), unique=True)
    status:     str = Column(Integer, ForeignKey('status.id'))

class UserForgotToken(settings.DBBaseModel):
    __tablename__ = 'usertokens'
    id:             int = Column(Integer, primary_key=True, autoincrement=True)
    user_id:        int = Column(Integer, ForeignKey('users.id'))
    token:          str = Column(String(100))
    expiredat:      DateTime = Column(DateTime)

