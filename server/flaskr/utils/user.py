from flaskr.extensions import db
from flaskr.models.user import User
from flaskr.models.rbac import Role
from flaskr.utils.rbac import search_role


# 查找用户
def search_user(*args, **kwargs) -> None | User:
    return db.session.query(User).filter_by(*args, **kwargs).first()


# 添加用户
def add_user(email: str, password: str, roles=["common"]):
    user = search_user(email=email)

    if user is not None:
        return user

    user = User(email=email, password=password)

    # 赋予用户角色
    for role in roles:
        # 从角色表中查询特定角色
        role = db.session.query(Role).filter_by(name=role).first()
        user.roles.append(role)

    db.session.add(user)
    db.session.flush()  # 获取最新插入的记录值
    db.session.commit()

    return user


# 添加超级管理员
def add_super_user():
    return add_user("root", "root123456", ["super"])


# 获取用户拥有的权限
def get_user_permission(user: User) -> list[str]:
    permissions = []

    for role in user.roles:
        for p in role.permissions:
            permissions.append(p.type)

    return permissions


# 获取用户角色
def get_user_role(user: User) -> list[str]:
    return [role.name for role in user.roles]


# 删除用户角色
def remove_user_role(user: User, roles: list[str]):
    for role in roles:
        role = search_role(name=role)

        if role in user.roles:
            user.roles.remove(role)

    db.session.commit()


# 给用户添加新角色
def add_new_role(user: User, roles: list[str]):
    for role in roles:
        role = search_role(name=role)

        if role not in user.roles:
            user.roles.append(role)

    db.session.commit()


# 查询所有用户
def search_all_user() -> None | list[User]:
    return db.session.query(User).all()


# 是否是某个角色
def is_role(user: User, type: str):
    for role in user.roles:
        if role.name == type:
            return True

    return False


# 是否是管理员
def is_manager(user: User):
    return is_role(user, "manager")


# 是否是超级管理员
def is_super_user(user: User):
    return is_role(user, "super")
