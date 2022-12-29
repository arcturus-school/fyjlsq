from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_jwt_extended import create_access_token
from ..models.user import (
    add_new_role,
    get_user_permission,
    get_user_role,
    remove_user_role,
    search_all_user,
    search_user,
    add_user,
)
from ..models.rbac import allow


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


# 用户注册
@auth_blueprint.route("/register", methods=["POST"])
def register():
    # TODO: 判断邮箱和密码的格式是否一定是字符串
    # TODO: 判断邮箱字段格式是否正确
    # TODO: 账号进行 MD5 加密
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    res = search_user(email=email)

    if res is not None:
        return jsonify(
            {
                "msg": "账号已注册",
                "code": 802,
            }
        )

    user = add_user(email, password)

    # 注册成功, 同时返回令牌, 方便直接登录
    token = create_access_token(
        identity={
            "email": email,
            "uid": user.uid,
        }
    )

    resp = {
        "token": token,
        "userInfo": {
            "email": user.email,
            "user_name": user.user_name,
            "avatar": user.avatar,
            "uid": user.uid,
            "create_at": user.create_at,
            "roles": get_user_role(user),
            "permissions": get_user_permission(user),
        },
        "code": 200,
        "msg": "注册成功",
    }

    return jsonify(resp)


# 登录
@auth_blueprint.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    res = search_user(email=email)

    if res is None:
        return jsonify(
            {
                "msg": "账号不存在",
                "code": 801,
            }
        )
    elif res.password != password:
        return jsonify(
            {
                "msg": "密码错误",
                "code": 800,
            }
        )

    # 登录成功, 返回令牌
    token = create_access_token(
        identity={
            "email": email,
            "uid": res.uid,
        }
    )

    resp = {
        "token": token,
        "userInfo": {
            "email": res.email,
            "user_name": res.user_name,
            "avatar": res.avatar,
            "uid": res.uid,
            "create_at": res.create_at,
            "roles": get_user_role(res),
            "permissions": get_user_permission(res),
        },
        "code": 200,
        "msg": "登录成功",
    }

    return jsonify(resp)


# 获取用户信息
@auth_blueprint.route("/user_info", methods=["GET"])
def get_user_info():
    uid = request.args.get("uid")

    user = search_user(uid=uid)

    if user is None:
        return jsonify(
            {
                "code": 801,
                "msg": "账号不存在",
            }
        )

    return jsonify(
        {
            "code": 200,
            "msg": "获取成功",
            "userInfo": {
                "email": user.email,
                "user_name": user.user_name,
                "avatar": user.avatar,
                "create_at": user.create_at,
                "uid": user.uid,
                "roles": get_user_role(user),
                "permissions": get_user_permission(user),
            },
        }
    )


# 获取成员列表
@auth_blueprint.route("/users", methods=["GET"])
@allow(["super"])
def get_user_list():
    all_users = search_all_user()

    res = []
    for user in all_users:
        if user.email == "root":
            continue
        else:
            res.append(
                {
                    "uid": user.uid,
                    "roles": get_user_role(user),
                    "email": user.email,
                    "avatar": user.avatar,
                    "user_name": user.user_name,
                }
            )

    return jsonify(
        {
            "code": 200,
            "msg": "获取全员列表成功",
            "users": res,
        }
    )


# 给用户新增/删除管理员权限
@auth_blueprint.route("/manager", methods=["POST"])
@allow(["super"])
def add_manager():
    uid = request.json.get("uid")
    type = request.json.get("type")

    if uid == 1:
        return jsonify(
            {
                "code": 900,
                "msg": "更新权限失败",
            }
        )

    user = search_user(uid=uid)

    if user is None:
        return jsonify(
            {
                "code": 801,
                "msg": "账号不存在",
            }
        )

    # TODO: 是否可能添加或删除失败?
    if type == "appoint":

        add_new_role(user, ["manager"])

        return jsonify(
            {
                "code": 200,
                "msg": "添加管理员成功",
            }
        )

    elif type == "remove":
        remove_user_role(user, ["manager"])

        return jsonify(
            {
                "code": 200,
                "msg": "删除管理员成功",
            }
        )
