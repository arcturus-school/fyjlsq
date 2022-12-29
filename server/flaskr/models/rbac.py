from functools import wraps
from flask import abort
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)
from flaskr.extensions import db
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR


# 用户-角色
user_role = db.Table(
    "user_role",
    db.Column(
        "user_id",
        INTEGER(unsigned=True),
        db.ForeignKey("users.uid"),
        nullable=False,
        comment="user's ID",
    ),
    db.Column(
        "role_id",
        INTEGER(unsigned=True),
        db.ForeignKey("roles.id"),
        nullable=False,
        comment="role's ID",
    ),
)

# 角色-权限
role_permission = db.Table(
    "role_permission",
    db.Column(
        "role_id",
        INTEGER(unsigned=True),
        db.ForeignKey("roles.id"),
        nullable=False,
        comment="role's ID",
    ),
    db.Column(
        "permission_id",
        INTEGER(unsigned=True),
        db.ForeignKey("permissions.id"),
        nullable=False,
        comment="permission's ID",
    ),
)


# 权限模型
class Permission(db.Model):
    __tablename__ = "permissions"

    id: int = db.Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    type: str = db.Column(
        VARCHAR(32),
        nullable=False,
        comment="权限",
    )


# 查找权限
def search_permission(*args, **kwargs) -> None | Permission:
    return Permission.query.filter_by(*args, **kwargs).first()


class Permissions:
    """权限类"""

    """普通用户权限"""
    POST = "post"  # 发帖
    COMMENT = "commit"  # 评论
    BROWSE = "browse"  # 浏览
    COLLECT = "collect"  # 收藏
    DELETE = "delete"  # 删帖

    """普通管理员权限"""
    DELETE_FREE = "delete_free"

    """超级管理员权限"""
    APPOINT = "appoint"  # 任命管理员
    REMOVE = "remove"  # 罢免管理员


permission_list = [
    Permissions.DELETE,
    Permissions.COMMENT,
    Permissions.BROWSE,
    Permissions.POST,
    Permissions.COLLECT,
    Permissions.DELETE_FREE,
    Permissions.APPOINT,
    Permissions.REMOVE,
]

role_permission_map = {
    "common": [0, 1, 2, 3, 4],
    "manager": [0, 1, 2, 3, 4, 5],
    "super": [0, 1, 2, 3, 4, 5, 6, 7],
}


# 角色模型
class Role(db.Model):
    __tablename__ = "roles"

    id: int = db.Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="role's ID",
    )

    name: str = db.Column(
        VARCHAR(32),
        unique=True,
        nullable=False,
        comment="role",
    )

    permissions: list[Permission] = db.relationship(
        "Permission",
        secondary=role_permission,
        backref=db.backref("roles", lazy="dynamic"),
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{__class__.__name__} {self.name}>"


# 查找角色
def search_role(*args, **kwargs) -> None | Role:
    return Role.query.filter_by(*args, **kwargs).first()


# 初始化角色
def init_role_permission():
    # 创建角色并关联权限
    for k, v in role_permission_map.items():
        role = search_role(name=k)

        if role is None:
            # 角色不存在, 则新增
            role = Role(name=k)
            db.session.add(role)

        for p in v:
            perm = search_permission(type=permission_list[p])

            if perm is None:
                role.permissions.append(Permission(type=permission_list[p]))
            else:
                # 角色已经存在, 直接关联
                role.permissions.append(perm)

    db.session.commit()


def allow(roles=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from .user import search_user

            verify_jwt_in_request()
            payload = get_jwt_identity()

            user = search_user(uid=payload.get("uid"))

            # 用户不存在
            if user is None:
                abort(403)

            for role in user.roles:
                if role.name in roles:
                    # 用户角色匹配
                    return f(*args, **kwargs)

            abort(403)  # 完全不匹配

        return decorated_function

    return decorator
