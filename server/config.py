from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "FYJLSQ")  # H256 加密算法密钥

days = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "365")

# make sure days is a number
if days.isnumeric():
    days = int(days)
else:
    days = 365

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=days)  # expiry date of token

# MYSQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")

port = os.getenv("MYSQL_PORT", "3306")

if port.isnumeric():
    port = int(port)
else:
    port = 3306

MYSQL_PORT = port
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "fyjlsq")

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"  # noqa E501
SQLALCHEMY_ECHO = False  # do not show original SQL statement

# 根目录
ROOT_PATH = os.path.dirname(__file__)
