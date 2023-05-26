from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import os

host        = os.environ['DB_HOST']
port        = os.environ['DB_PORT']
user        = os.environ['DB_USER']
password    = os.environ['DB_PASSWORD']
db_name     = os.environ['DB_NAME']

string_conexao = 'mysql+aiomysql://{user}:{password}@{host}/{db_name}'.format(
    user=user,
    password=password,
    host=host,
    port=port,
    db_name=db_name
)

class Settings(BaseSettings):
    API_V1:                         str = '/api/v1'
    DB_URL:                         str = string_conexao
    DBBaseModel                         = declarative_base()
    JWT_SECRET:                     str = 'z_QRxrghr6NUo48ncegFTWxGCHr9kh-4-XnAfM21qLM'
    ALGORITHM:                      str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:    int = 60* 24 * 7


    class Config:
        case_sensitive = True

settings = Settings()
