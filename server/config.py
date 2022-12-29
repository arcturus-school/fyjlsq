"""
配置信息
"""

from datetime import timedelta
import os

# JWT
JWT_SECRET_KEY = "FYJLSQ"  # H256 加密算法密钥
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)  # token 有效期一年

# MYSQL
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "fyjlsq"
MYSQL_DB = "fyjlsq"

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"  # noqa E501
SQLALCHEMY_ECHO = False  # 不显示原始 sql 语句

# 根目录
ROOT_PATH = os.path.dirname(__file__)
