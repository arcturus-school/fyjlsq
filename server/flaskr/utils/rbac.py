from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flaskr.models.rbac import Permission, Role
from flaskr.extensions import db

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
