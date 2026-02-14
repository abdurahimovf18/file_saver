from typing import Literal

from pydantic_settings import BaseSettings


class Env(BaseSettings):
    # system
    DEBUG: Literal["true", "false"]

    # db
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # s3
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_HOST: str
    S3_PORT: int

env = Env()  # type: ignore

# system
DEBUG = env.DEBUG == "true"

# db
DB_USER = env.DB_USER
DB_PASSWORD = env.DB_PASSWORD
DB_HOST = env.DB_HOST
DB_PORT = env.DB_PORT
DB_NAME = env.DB_NAME

# s3
S3_ACCESS_KEY = env.S3_ACCESS_KEY
S3_SECRET_KEY = env.S3_SECRET_KEY
S3_HOST = env.S3_HOST
S3_PORT = env.S3_PORT
