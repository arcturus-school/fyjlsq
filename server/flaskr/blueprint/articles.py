from flask import (
    Blueprint,
    abort,
    jsonify,
    request,
)
from flask_jwt_extended import get_jwt_identity

from flaskr.models.rbac import allow
from flaskr.models.article import (
    add_article,
    get_article_list,
    get_ones_articles_count,
    remove_article,
    search_article,
    get_ones_articles,
    edit_article,
)
from flaskr.models.user import (
    is_manager,
    is_super_user,
    search_user,
)

article_blueprint = Blueprint("article", __name__, url_prefix="/article")


# 获取文章列表
@article_blueprint.route("/list", methods=["GET"])
def get_articles():

    res = get_article_list()

    articles = []

    for article, user in res:
        articles.append(
            {
                "cover": article.cover,
                "id": article.id,
                "title": article.title,
                "abstract": article.abstract,
                "update_at": article.update_at,
                "character_count": article.character_count,
                "create_at": article.create_at,
                "user": {
                    "email": user.email,
                    "uid": user.uid,
                    "avatar": user.avatar,
                    "user_name": user.user_name,
                },
            }
        )

    return jsonify(
        {
            "code": 200,
            "msg": "获取文章成功",
            "articles": articles,
        }
    )


# 获取某个人的文章
@article_blueprint.route("/user/list", methods=["GET"])
def ones_articles():
    uid = request.args.get("uid")
    page = request.args.get("page", 1)

    user = search_user(uid=uid)

    if user is None:
        abort(404)

    res = get_ones_articles(user, page)

    articles = []
    num = 0
    for article in res:
        num = num + 1
        articles.append(
            {
                "content": article.content,
                "cover": article.cover,
                "id": article.id,
                "title": article.title,
                "character_count": article.character_count,
                "abstract": article.abstract,
                "update_at": article.update_at,
                "create_at": article.create_at,
            }
        )

    count = get_ones_articles_count(user=user)

    return jsonify(
        {
            "code": 200,
            "msg": "获取文章成功",
            "articles": articles,
            "user": {
                "email": user.email,
                "uid": user.uid,
                "avatar": user.avatar,
                "user_name": user.user_name,
            },
            "page": {
                "count": count,
                "page_num": page,
                "cur_num": num,
            },
        }
    )


# 编辑帖子
@article_blueprint.route("/edit", methods=["POST"])
@allow(["common", "manager", "super"])
def edit():
    content = request.json.get("content")
    cover = request.json.get("cover")
    title = request.json.get("title")
    abstract = request.json.get("abstract")
    character_count = request.json.get("characters")
    id = request.json.get("id")

    payload = get_jwt_identity()

    user = search_user(uid=payload.get("uid"))

    if user is None:
        return jsonify(
            {
                "code": 801,
                "msg": "无效账号",
            }
        )

    article = user.articles.filter_by(id=id).first()

    if article is None:
        return jsonify(
            {
                "code": 820,
                "msg": "文章不存在",
            }
        )

    edit_article(
        article,
        content,
        title,
        cover,
        abstract,
        character_count,
    )

    return jsonify(
        {
            "code": 200,
            "msg": "修改成功",
        }
    )


# 发帖
@article_blueprint.route("/post", methods=["POST"])
@allow(["common", "manager", "super"])
def post():
    content = request.json.get("content")
    cover = request.json.get("cover")
    title = request.json.get("title")
    abstract = request.json.get("abstract")
    character_count = request.json.get("characters")

    payload = get_jwt_identity()

    user = search_user(uid=payload.get("uid"))

    if user is None:
        return jsonify(
            {
                "code": 801,
                "msg": "无效账号",
            }
        )

    article = add_article(
        user,
        content,
        title,
        cover,
        abstract,
        character_count,
    )

    return jsonify(
        {
            "code": 200,
            "msg": "发帖成功",
            "id": article.id,
        }
    )


# 帖子详情
@article_blueprint.route("/<id>", methods=["GET"])
def article_detail_info(id):
    article = search_article(id=id)

    if article is None:
        abort(404)

    user = search_user(uid=article.uid)

    return jsonify(
        {
            "code": 200,
            "msg": "获取成功",
            "article": {
                "id": article.id,
                "content": article.content,
                "cover": article.cover,
                "abstract": article.abstract,
                "character_count": article.character_count,
                "title": article.title,
                "update_at": article.update_at,
                "create_at": article.create_at,
                "user": {
                    "uid": user.uid,
                    "email": user.email,
                    "avatar": user.avatar,
                    "user_name": user.user_name,
                },
            },
        }
    )


# 删除帖子
@article_blueprint.route("/delete", methods=["POST", "DELETE"])
@allow(["common", "manager", "super"])
def delete_article():
    id = request.json.get("id", None)
    payload = get_jwt_identity()

    article = search_article(id=id)

    if article is None:
        return jsonify(
            {
                "code": 820,
                "msg": "文章不存在",
            }
        )

    user = search_user(uid=payload.get("uid"))

    if user.uid != article.uid:
        # 文章不属于该 user, 需要有管理员或超级管理员权限
        if not is_manager(user) and not is_super_user(user):
            abort(403)

    remove_article(id=article.id)

    return jsonify(
        {
            "code": 200,
            "msg": "删除成功",
        }
    )
