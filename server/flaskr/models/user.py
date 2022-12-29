from datetime import datetime
from flaskr.extensions import db
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, VARCHAR

from flaskr.models.rbac import Role, user_role, search_role
from flaskr.utils.func import (
    get_random_user_name,
    get_user_default_avatar,
)


# 用户模型
class User(db.Model):
    __tablename__ = "users"

    uid: int = db.Column(
        INTEGER(unsigned=True),
        primary_key=True,
    )

    roles: list[Role] = db.relationship(
        "Role",
        secondary=user_role,
        backref=db.backref("users", lazy="dynamic"),
    )

    email: str = db.Column(
        VARCHAR(255),
        unique=True,
        nullable=False,
        comment="邮箱",
    )

    password: str = db.Column(
        VARCHAR(255),
        nullable=False,
        comment="密码",
    )

    user_name: str = db.Column(
        VARCHAR(255),
        nullable=False,
        default=get_random_user_name,
        comment="用户名",
    )

    avatar: str = db.Column(
        VARCHAR(255),
        default=get_user_default_avatar,
        comment="用户头像",
    )

    create_at: datetime = db.Column(
        DATETIME(),
        default=datetime.now,
        comment="创建时间",
    )

    register_ip: str = db.Column(
        VARCHAR(255),
        comment="用户注册时 IP 地址",
    )

    update_at: datetime = db.Column(
        DATETIME(),
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    )

    email_verified_at: datetime = db.Column(
        DATETIME(),
        comment="邮箱确认时间",
    )

    def __repr__(self):
        return f"<User {self.email}"


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
# TODO: 分页查询
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
