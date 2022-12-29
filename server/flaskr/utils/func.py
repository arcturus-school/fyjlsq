import random
import string
from flaskr.utils.constant import DEFAULT_AVATAR_URL


def get_random_user_name(num: int = 6):
    return "".join(random.sample(string.ascii_letters, num))


def get_user_default_avatar():
    return DEFAULT_AVATAR_URL[random.randint(0, len(DEFAULT_AVATAR_URL) - 1)]
