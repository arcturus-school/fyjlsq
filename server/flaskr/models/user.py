from datetime import datetime
from flaskr.extensions import db
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from flaskr.models.rbac import Role, user_role
from flaskr.utils.func import random_user_name, random_user_avatar


# 用户模型
class User(db.Model):
    __tablename__ = "fyjlsq_users"

    uid: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        comment="primary key",
    )

    roles: Mapped[list[Role]] = db.relationship(
        "Role",
        secondary=user_role,
        backref=db.backref("fyjlsq_users", lazy="dynamic"),
    )

    email: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
        nullable=False,
        comment="email",
    )

    password: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="password",
    )

    user_name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        default=random_user_name,
        comment="username",
    )

    avatar: Mapped[str] = mapped_column(
        VARCHAR(255),
        default=random_user_avatar,
        comment="avatar",
    )

    create_at: Mapped[datetime] = mapped_column(
        DATETIME(),
        default=datetime.now,
        comment="user create time",
    )

    update_at: Mapped[datetime] = mapped_column(
        DATETIME(),
        default=datetime.now,
        onupdate=datetime.now,
        comment="user info update time",
    )

    def __repr__(self):
        return f"<User {self.email}"
