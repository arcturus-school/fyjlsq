from flaskr.extensions import db
from flaskr.models.article import Article, User

# 查询文章
def search_article(*arg, **kwargs) -> None | Article:
    return db.session.query(Article).filter_by(*arg, **kwargs).first()


# 查询某个人的文章数
def get_ones_articles_count(user: User) -> int:
    return user.articles.count()


# 查询某个人的所有文章
def get_ones_articles(user: User, page: int, per_page: int = 50) -> list[Article]:
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
def get_article_list() -> list[tuple[Article, User]]:
    return (
        db.session.query(Article, User).filter(Article.uid == User.uid).all()
    )  # noqa E501


# 删除文章
def remove_article(*arg, **kwargs):
    db.session.query(Article).filter_by(*arg, **kwargs).delete()

    db.session.commit()
