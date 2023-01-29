from .constant import DEFAULT_AVATAR_URL
from random import sample, randint
from string import ascii_letters


def random_user_name(num: int = 6):
    return "".join(sample(ascii_letters, num))


def random_user_avatar():
    return DEFAULT_AVATAR_URL[randint(0, len(DEFAULT_AVATAR_URL) - 1)]
