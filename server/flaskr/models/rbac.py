from flaskr.extensions import db
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

# 用户-角色
user_role = db.Table(
    "fyjlsq_user_role",
    db.Column(
        "user_id",
        INTEGER(unsigned=True),
        db.ForeignKey("fyjlsq_users.uid"),
        nullable=False,
        comment="user's ID",
    ),
    db.Column(
        "role_id",
        INTEGER(unsigned=True),
        db.ForeignKey("fyjlsq_roles.id"),
        nullable=False,
        comment="role's ID",
    ),
)

# 角色-权限
role_permission = db.Table(
    "fyjlsq_role_permission",
    db.Column(
        "role_id",
        INTEGER(unsigned=True),
        db.ForeignKey("fyjlsq_roles.id"),
        nullable=False,
        comment="role's ID",
    ),
    db.Column(
        "permission_id",
        INTEGER(unsigned=True),
        db.ForeignKey("fyjlsq_permissions.id"),
        nullable=False,
        comment="permission's ID",
    ),
)


# 权限模型
class Permission(db.Model):
    __tablename__ = "fyjlsq_permissions"

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    type: Mapped[str] = mapped_column(
        VARCHAR(32),
        nullable=False,
        comment="type of permissions",
    )


# 角色模型
class Role(db.Model):
    __tablename__ = "fyjlsq_roles"

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="role's ID",
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(32),
        unique=True,
        nullable=False,
        comment="role",
    )

    permissions: Mapped[list[Permission]] = db.relationship(
        "Permission",
        secondary=role_permission,
        backref=db.backref("fyjlsq_roles", lazy="dynamic"),
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{__class__.__name__} {self.name}>"
