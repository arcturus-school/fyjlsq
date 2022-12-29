from datetime import datetime
from uuid import uuid4
from flaskr.models.user import User
from flaskr.extensions import db
from sqlalchemy.dialects.mysql import (
    INTEGER,
    LONGTEXT,
    TEXT,
    CHAR,
    VARCHAR,
    DATETIME,
)


# 文章模型
class Article(db.Model):
    __tablename__ = "articles"

    id: str = db.Column(
        CHAR(32),
        default=lambda: uuid4().hex,
        primary_key=True,
        comment="主键",
    )

    uid: int = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("users.uid"),
        nullable=False,
    )

    user: list[User] = db.relationship(
        "User",
        backref=db.backref(
            "articles",
            lazy="dynamic",
        ),
    )

    title: str = db.Column(
        LONGTEXT(),
        nullable=False,
        comment="文章标题",
    )

    character_count: int = db.Column(
        INTEGER(unsigned=True),
        nullable=False,
    )

    content: str = db.Column(
        LONGTEXT(),
        nullable=False,
        comment="文章内容",
    )

    abstract: str = db.Column(
        VARCHAR(255),
        nullable=False,
        comment="摘要",
    )

    tags: str = db.Column(TEXT(), comment="文章标签")

    cover: str = db.Column(
        VARCHAR(255),
        nullable=False,
        comment="封面图地址",
    )

    create_at: datetime = db.Column(
        DATETIME(),
        default=datetime.now,
        comment="创建时间",
    )

    update_at: datetime = db.Column(
        DATETIME(),
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    )


# 查询文章
def search_article(*arg, **kwargs) -> None | Article:
    return db.session.query(Article).filter_by(*arg, **kwargs).first()


# 查询某个人的文章数
def get_ones_articles_count(user: User) -> int:
    return user.articles.count()


# 查询某个人的所有文章
def get_ones_articles(
    user: User,
    page: int,
    per_page: int = 50,
) -> list[Article]:
    return user.articles.order_by(Article.create_at.desc()).paginate(
        page=page,
        per_page=per_page,
    )


# 发帖
def add_article(
    user: User,
    content: str,
    title: str,
    cover: str,
    abstract: str,
    character_count: int,
):

    article = Article(
        content=content,
        cover=cover,
        title=title,
        abstract=abstract,
        character_count=character_count,
        uid=user.uid,
    )

    user.articles.append(article)

    db.session.flush()
    db.session.commit()

    return article


# 编辑帖子
def edit_article(
    article: Article,
    content: str,
    title: str,
    cover: str,
    abstract: str,
    character_count: int,
):
    article.content = content
    article.title = title
    article.cover = cover
    article.abstract = abstract
    article.character_count = character_count

    db.session.flush()
    db.session.commit()


# 获取文章列表
# TODO: 分页查询
def get_article_list() -> list[tuple[Article, User]]:
    return (
        db.session.query(Article, User).filter(Article.uid == User.uid).all()
    )  # noqa E501


# 删除文章
def remove_article(*arg, **kwargs):
    db.session.query(Article).filter_by(*arg, **kwargs).delete()

    db.session.commit()
