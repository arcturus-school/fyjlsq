import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .models.rbac import init_role_permission
from .models.user import add_super_user
from .blueprint import blueprint_init
from .error_handler import error_handle_init
from .extensions import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)  # 创建 flask 实例
    app.config.from_object("config")

    JWTManager(app)  # 初始化 JWT

    CORS(app, resources=r"/*")  # 解决前端跨域问题

    blueprint_init(app)  # 初始化蓝图

    error_handle_init(app)  # 初始化错误处理器

    db.init_app(app)  # 初始化 mysql

    with app.app_context():
        if os.getenv("FLASK_DEBUG"):
            db.drop_all()  # 仅开发者模式下才需要删除原来的表

        db.create_all()  # 创建所有表

        init_role_permission()  # 初始化角色与权限
        add_super_user()  # 新建超级管理员

    return app
