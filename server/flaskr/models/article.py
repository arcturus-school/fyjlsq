from datetime import datetime
from uuid import uuid4
from flaskr.models.user import User
from flaskr.extensions import db
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, CHAR, VARCHAR, DATETIME
from sqlalchemy.orm import Mapped, mapped_column


class Article(db.Model):
    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(
        CHAR(32),
        default=lambda: uuid4().hex,
        primary_key=True,
        comment="primary key",
    )

    uid: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        db.ForeignKey("users.uid"),
        nullable=False,
    )

    user: Mapped[list[User]] = db.relationship(
        "User", backref=db.backref("articles", lazy="dynamic")
    )

    title: Mapped[str] = mapped_column(
        LONGTEXT(),
        nullable=False,
        comment="article title",
    )

    character_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        LONGTEXT(),
        nullable=False,
        comment="article content",
    )

    abstract: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="article abstract",
    )

    tags: Mapped[str] = mapped_column(
        TEXT(),
        comment="article tags",
        nullable=True,
    )

    cover: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="article cover",
    )

    create_at: Mapped[datetime] = mapped_column(
        DATETIME(),
        default=datetime.now,
        comment="article creation time",
    )

    update_at: Mapped[datetime] = mapped_column(
        DATETIME(),
        default=datetime.now,
        onupdate=datetime.now,
        comment="article update time",
    )
